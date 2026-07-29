from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_requirements_index.py"
SPEC = importlib.util.spec_from_file_location("update_requirements_index", SCRIPT)
assert SPEC and SPEC.loader
update_requirements_index = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = update_requirements_index
SPEC.loader.exec_module(update_requirements_index)


class RequirementsIndexTest(unittest.TestCase):
    def test_application_area_parser_reads_requirement_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "layers.md"
            path.write_text(
                """# Layer Reading Requirements

## LAYER-001 — Show an orthophoto

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: MVP

## LAYER-002 — Explain unavailable addresses

- Status: VERIFIED
- Priority: SHOULD
- Delivery stage: MVP
""",
                encoding="utf-8",
            )

            requirements = update_requirements_index.parse_area_file(path)

        self.assertEqual([item.identifier for item in requirements], ["LAYER-001", "LAYER-002"])
        self.assertEqual(requirements[0].area, "Layer Reading")
        self.assertEqual(requirements[1].status, "VERIFIED")

    def test_summary_aggregates_areas_stages_statuses_and_verified_completion(self) -> None:
        requirements = [
            update_requirements_index.Requirement(
                "LAYER-001", "Show an orthophoto", "Layer Reading", "layer-reading.md",
                "VERIFIED", "MUST", "MVP",
            ),
            update_requirements_index.Requirement(
                "SKETCH-001", "Draw a path", "Sketches", "sketches.md",
                "IMPLEMENTED", "MUST", "STAGE-2",
            ),
        ]

        summary = update_requirements_index.render_summary(requirements)

        self.assertIn("## Application Area Summary", summary)
        self.assertIn("| Application area | Total | Verified | Completion | Area file |", summary)
        self.assertIn("| Layer Reading | 1 | 1 | 100% |", summary)
        self.assertIn("| Sketches | 1 | 0 | 0% |", summary)
        self.assertIn("| **All areas** | **2** | **1** | **50%** |", summary)
        self.assertIn("| `MVP` | Basic source-layer reading and interpretation | 1 | 1 |", summary)
        self.assertIn("| `IMPLEMENTED` | 1 |", summary)
        self.assertIn("| `VERIFIED` | 1 |", summary)

    def test_generated_region_replacement_preserves_surrounding_content(self) -> None:
        original = f"""# Requirements Index

Before
{update_requirements_index.SUMMARY_START}

old

{update_requirements_index.SUMMARY_END}
After
"""

        updated = update_requirements_index.replace_summary(original, "new")

        self.assertIn("Before", updated)
        self.assertIn("After", updated)
        self.assertIn(f"{update_requirements_index.SUMMARY_START}\n\nnew\n\n", updated)
        self.assertNotIn("\nold\n", updated)

    def test_duplicate_ids_across_application_areas_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            content = """# {area} Requirements

## SHARED-001 — Capability

- Status: DRAFT
- Priority: MUST
- Delivery stage: MVP
"""
            (directory_path / "one.md").write_text(
                content.format(area="First Area"), encoding="utf-8"
            )
            (directory_path / "two.md").write_text(
                content.format(area="Second Area"), encoding="utf-8"
            )

            with self.assertRaisesRegex(ValueError, "Duplicate requirement IDs: SHARED-001"):
                update_requirements_index.load_requirements(directory_path)


if __name__ == "__main__":
    unittest.main()
