"""Synthetic auditor tests. These do not run or evaluate a language model."""

import copy
import unittest

from check_trace import audit


def good_trace(step="S1", offset=0, before="a", after="b"):
    records = [
        {"kind": "begin", "requirements": ["R1"], "targets": ["writer.py"],
         "checks": ["T1"], "sources": {"spec": "v1"}},
        {"kind": "read_doc", "source": "spec", "revision": "v1",
         "section": "Output", "complete": True},
        {"kind": "read_target", "target": "writer.py", "revision": before, "complete": True},
        {"kind": "mutate", "before": {"writer.py": before}, "after": {"writer.py": after}},
        {"kind": "inspect", "revisions": {"writer.py": after}},
        {"kind": "check", "check": "T1", "status": "PASS",
         "revisions": {"writer.py": after}, "test_count": 2, "exit_code": 0},
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
        next_rows = good_trace("S2", len(rows), "b", "c")
        next_rows[0]["depends_on"] = ["S1"]
        self.assert_invalid(rows + next_rows, "failed prerequisite")

    def test_each_step_requires_new_reads(self):
        rows = good_trace()
        next_rows = good_trace("S2", len(rows), "b", "c")
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


    # --- Levels (v2) ---

    def test_l1_reuses_doc_verified_earlier_in_task(self):
        rows = good_trace()
        follow = good_trace("S2", len(rows), "b", "c")
        del follow[1]  # no re-read of "spec"; it was read at v1 in S1
        follow[0]["level"] = "L1"
        follow[1]["revision"] = "b"
        follow[2]["before"] = {"writer.py": "b"}
        follow[2]["after"] = follow[3]["revisions"] = follow[4]["revisions"] = {"writer.py": "c"}
        self.assertTrue(audit(rows + follow)["process_compliant"], audit(rows + follow))

    def test_l1_cannot_rely_on_unverified_source(self):
        rows = good_trace()
        rows[0]["level"] = "L1"
        del rows[1]
        self.assert_invalid(rows, "not verified earlier")

    def test_l1_still_requires_fresh_target_read(self):
        rows = good_trace()
        follow = good_trace("S2", len(rows), "a", "c")  # reads the revision S1 already replaced
        del follow[1]
        follow[0]["level"] = "L1"
        self.assert_invalid(rows + follow, "stale target read")

    def test_l1_without_target_read_is_rejected(self):
        rows = good_trace()
        follow = good_trace("S2", len(rows), "b", "c")
        del follow[1:3]
        follow[0]["level"] = "L1"
        follow[1]["before"] = {"writer.py": "b"}
        follow[1]["after"] = follow[2]["revisions"] = follow[3]["revisions"] = {"writer.py": "c"}
        self.assert_invalid(rows + follow, "missing or stale target read")

    def test_l1_retry_after_failure_is_rejected(self):
        rows = good_trace()
        rows[5].update(status="FAIL", exit_code=1)
        rows[6].update(status="FAIL", reason="assertion failed")
        retry = good_trace("S2", len(rows), "b", "c")
        retry[0]["level"] = "L1"
        self.assert_invalid(rows + retry, "retry after a failure")

    def test_l3_requires_authorization_and_recovery(self):
        rows = good_trace()
        rows[0]["level"] = "L3"
        self.assert_invalid(copy.deepcopy(rows), "authorization")
        rows[0]["authorization"] = "user message 3"
        self.assert_invalid(copy.deepcopy(rows), "recovery")
        rows[0]["recovery"] = "git checkout -- writer.py (only this task's change)"
        self.assertTrue(audit(rows)["process_compliant"])

    def test_unknown_level(self):
        rows = good_trace()
        rows[0]["level"] = "L9"
        self.assert_invalid(rows, "level must be")

    def test_empty_sources_need_reason(self):
        rows = good_trace()
        rows[0]["sources"] = {}
        del rows[1]
        self.assert_invalid(copy.deepcopy(rows), "no_source_reason")
        rows[0]["no_source_reason"] = "pure rename of a private local variable"
        self.assertTrue(audit(rows)["process_compliant"])

    def test_read_only_step(self):
        rows = [
            {"kind": "begin", "level": "L0", "requirements": ["Q1"], "targets": [],
             "checks": [], "sources": {"spec": "v1"}},
            {"kind": "read_doc", "source": "spec", "revision": "v1", "section": "Exit codes", "complete": True},
            {"kind": "end", "status": "PASS"},
        ]
        rows = [dict(r, seq=i, step="Q", receipt=f"synthetic:Q:{i}") for i, r in enumerate(rows, 1)]
        self.assertTrue(audit(rows)["process_compliant"])
        self.assert_invalid(rows[:1] + rows[2:], "without any recorded read")

    def test_read_only_step_cannot_mutate(self):
        rows = good_trace()
        rows[0]["level"] = "L0"
        self.assert_invalid(rows, "read-only")

    # --- Reporting every violation ---

    def test_all_errors_reports_each_invalid_step(self):
        first = good_trace()
        del first[1]  # missing doc read
        second = good_trace("S2", len(first), "b", "c")
        second[5]["test_count"] = 0  # zero-test PASS
        third = good_trace("S3", len(first) + len(second), "c", "d")
        result = audit(first + second + third, all_errors=True)
        self.assertFalse(result["process_compliant"])
        self.assertEqual(len(result["errors"]), 2, result)
        self.assertIn("documentation not re-read", result["errors"][0])
        self.assertIn("zero or invalid test count", result["errors"][1])
        self.assertEqual(result["closed_steps"], 1)

    def test_all_errors_dependency_on_invalid_step_fails(self):
        first = good_trace()
        del first[1]
        second = good_trace("S2", len(first), "b", "c")
        second[0]["depends_on"] = ["S1"]
        result = audit(first + second, all_errors=True)
        self.assertEqual(len(result["errors"]), 2, result)
        self.assertIn("failed prerequisite", result["errors"][1])

    def test_default_mode_stops_at_first_error(self):
        first = good_trace()
        del first[1]
        second = good_trace("S2", len(first), "b", "c")
        second[5]["test_count"] = 0
        self.assertEqual(len(audit(first + second)["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
