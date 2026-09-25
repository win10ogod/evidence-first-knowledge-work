"""Synthetic auditor tests. These do not run or evaluate a language model."""

import copy
import unittest

from check_trace import audit


def good_trace(step="S1", offset=0):
    records = [
        {"kind": "begin", "requirements": ["R1"], "targets": ["writer.py"],
         "checks": ["T1"], "sources": {"spec": "v1"}},
        {"kind": "read_doc", "source": "spec", "revision": "v1",
         "section": "Output", "complete": True},
        {"kind": "read_target", "target": "writer.py", "revision": "a", "complete": True},
        {"kind": "mutate", "before": {"writer.py": "a"}, "after": {"writer.py": "b"}},
        {"kind": "inspect", "revisions": {"writer.py": "b"}},
        {"kind": "check", "check": "T1", "status": "PASS",
         "revisions": {"writer.py": "b"}, "test_count": 2, "exit_code": 0},
        {"kind": "end", "status": "PASS"},
    ]
    return [dict(row, seq=offset+i, step=step, receipt=f"synthetic:{step}:{i}")
            for i, row in enumerate(records, 1)]


class TraceTests(unittest.TestCase):
    def assert_invalid(self, records, phrase):
        result = audit(records)
        self.assertFalse(result["process_compliant"], result)
        self.assertIn(phrase, result["errors"][0])

    def test_valid_trace_is_not_capability_evidence(self):
        result = audit(good_trace())
        self.assertTrue(result["process_compliant"])
        self.assertEqual(result["task_outcome"], "NOT MEASURED")
        self.assertEqual(result["receipt_authenticity"], "NOT VERIFIED")

    def test_missing_docs(self):
        rows = good_trace()
        del rows[1]
        self.assert_invalid(rows, "documentation not re-read")

    def test_docs_after_write(self):
        rows = good_trace()
        rows[1], rows[3] = rows[3], rows[1]
        for i, row in enumerate(rows, 1):
            row["seq"] = i
        self.assert_invalid(rows, "documentation not re-read")

    def test_incomplete_document(self):
        rows = good_trace()
        rows[1]["complete"] = False
        self.assert_invalid(rows, "incomplete source read")

    def test_wrong_source_version(self):
        rows = good_trace()
        rows[1]["revision"] = "v2"
        self.assert_invalid(rows, "source version mismatch")

    def test_stale_target(self):
        rows = good_trace()
        rows[3]["before"]["writer.py"] = "newer"
        self.assert_invalid(rows, "stale target read")

    def test_missing_target(self):
        rows = good_trace()
        del rows[2]
        self.assert_invalid(rows, "stale target read")

    def test_scope_escape(self):
        rows = good_trace()
        rows[3]["before"] = {"other.py": "a"}
        rows[3]["after"] = {"other.py": "b"}
        self.assert_invalid(rows, "exceeds target scope")

    def test_missing_inspection(self):
        rows = good_trace()
        del rows[4]
        self.assert_invalid(rows, "precedes change inspection")

    def test_stale_validation(self):
        rows = good_trace()
        rows[5]["revisions"] = {"writer.py": "a"}
        self.assert_invalid(rows, "stale revision")

    def test_zero_tests(self):
        rows = good_trace()
        rows[5]["test_count"] = 0
        self.assert_invalid(rows, "zero or invalid test count")

    def test_nonzero_exit(self):
        rows = good_trace()
        rows[5]["exit_code"] = 1
        self.assert_invalid(rows, "contradicts exit code")

    def test_not_run_cannot_pass(self):
        rows = good_trace()
        rows[5]["status"] = "NOT RUN"
        self.assert_invalid(rows, "unpassed validation")

    def test_missing_planned_check(self):
        rows = good_trace()
        rows[0]["checks"].append("T2")
        self.assert_invalid(rows, "planned validation is missing")

    def test_honest_failure_is_process_compliant(self):
        rows = good_trace()
        rows[5]["status"] = "FAIL"
        rows[5]["exit_code"] = 1
        rows[6].update(status="FAIL", reason="Output contradicts specification")
        self.assertTrue(audit(rows)["process_compliant"])

    def test_failed_dependency_blocks_mutation(self):
        rows = good_trace()
        rows[5]["status"] = "FAIL"
        rows[-1].update(status="FAIL", reason="Observed failure")
        next_rows = good_trace("S2", len(rows))
        next_rows[0]["depends_on"] = ["S1"]
        self.assert_invalid(rows + next_rows, "failed prerequisite")

    def test_each_step_requires_new_reads(self):
        rows = good_trace()
        next_rows = good_trace("S2", len(rows))
        del next_rows[1]
        self.assert_invalid(rows + next_rows, "documentation not re-read")

    def test_missing_receipt(self):
        rows = good_trace()
        rows[2]["receipt"] = ""
        self.assert_invalid(rows, "missing original runner/tool receipt")

    def test_bad_sequence(self):
        rows = good_trace()
        rows[2]["seq"] = rows[1]["seq"]
        self.assert_invalid(rows, "strictly increase")

    def test_unfinished_trace(self):
        self.assert_invalid(good_trace()[:-1], "unfinished step")

    def test_empty_and_malformed_inputs(self):
        for value in ([], None, {}, [None], ["event"]):
            with self.subTest(value=value):
                self.assertFalse(audit(value)["process_compliant"])

    def test_unknown_event(self):
        rows = good_trace()
        rows[2]["kind"] = "magic"
        self.assert_invalid(rows, "unsupported event kind")

    def test_new_file_requires_observed_absence(self):
        rows = good_trace()
        rows[2]["revision"] = "ABSENT"
        rows[3]["before"]["writer.py"] = "ABSENT"
        self.assertTrue(audit(rows)["process_compliant"])

    def test_two_file_atomic_mutation(self):
        rows = good_trace()
        rows[0]["targets"].append("test_writer.py")
        extra = dict(rows[2], target="test_writer.py", revision="t1")
        rows.insert(3, extra)
        rows[4]["before"]["test_writer.py"] = "t1"
        rows[4]["after"]["test_writer.py"] = "t2"
        for row in rows[5:7]:
            row["revisions"]["test_writer.py"] = "t2"
        for i, row in enumerate(rows, 1):
            row["seq"] = i
        self.assertTrue(audit(rows)["process_compliant"])

    def test_repeat_mutation_requires_fresh_step(self):
        rows = good_trace()
        extra = copy.deepcopy(rows[3])
        extra["seq"] = rows[3]["seq"] + 1
        rows.insert(4, extra)
        for i, row in enumerate(rows, 1):
            row["seq"] = i
        self.assert_invalid(rows, "fresh step")

    def test_honest_blocked_step(self):
        rows = good_trace()[:1]
        rows.append({"seq": 2, "kind": "end", "step": "S1", "status": "BLOCKED",
                     "reason": "Exact-version source unavailable", "receipt": "synthetic:block"})
        self.assertTrue(audit(rows)["process_compliant"])


if __name__ == "__main__":
    unittest.main()
