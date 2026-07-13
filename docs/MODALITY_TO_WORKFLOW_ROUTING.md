# Modality-To-Workflow Routing

Routing rules mapping modality signals onto proposed action workflows.

## 1. Mappings routing
- Document/PDF -> `create_lesson_note` (requires no approval).
- Screenshot/Image -> `build_practice_plan` (requires approval).
- Voice Transcript -> triggers workflow step resumption.
- Text -> proposals mapping generic summaries.
