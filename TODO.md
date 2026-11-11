# To do

Your list of ideas and tasks, for you first: numbered so you can say "do 2", in any order. The agent reads it too and can suggest what to do next, but it confirms with you before starting an item and removes the item once it's done. When nothing is planned, the list says *Nothing planned.*

1. Add `docs/features.md`: the agreed feature list in priority order, one line each with its status (`next`, `building`, `done`, `dropped`) and its plan or PR; `status.md` points to it instead of listing features.
2. Add `docs/security-checklist.md`: the go-live gate to clear before real users, customer data, payments or a `prod` deploy; a prototype works through it at the rule 24 stop, production before its first `prod` deploy.
