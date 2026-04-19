# Campaign Onboarding Playbook

Step-by-step workflow for launching a new real estate campaign in KPH Sales OS.

## When to use
Run this playbook end-to-end when onboarding a new project (e.g., KP-XXX-NNN).

## Order of execution
1. `00_claudechat_project_interview.md` — Claude Chat interviews Liam to gather raw project data
2. `01_cowork_rename_images.md` — Cowork renames images to KP-XXX-NNN convention
3. `02_claudecode_upload_firebase.md` — Claude Code uploads project record to Firebase
4. `04_claudecode_update_firebase_fields_v4.md` — Update full field set on /Projects_Public
5. `05_claudecode_decision_tree_objections.md` — Build decision tree + objections cheat sheet
6. `06_claudecode_jade_prompt_section.md` — Add new section to Maya master prompt
7. `07_brief_yair.md` — Generate Facebook ads brief for Yair
8. `08_linear_ticket_adam.md` — Open Linear ticket for Adam if backend changes needed

`PROJECT_ONBOARDING_CHECKLIST.md` is the master checklist tying all phases together.

## How to invoke
Tell Claude Chat: "חדש: אני מעלה פרויקט [KP-XXX-NNN]. תקרא את ה-playbook"

Claude will fetch this README + relevant phase files via web_fetch as the workflow progresses.
