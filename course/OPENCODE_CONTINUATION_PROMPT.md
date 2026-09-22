# OpenCode Continuation Prompt

Use this prompt when asking OpenCode to continue the AgentCore course after Day 5.

---

Continue the Amazon Bedrock AgentCore course in this repository.

Before changing anything, read these files in order:

1. `course/README.md`
2. `course/TEACHING_STANDARD.md`
3. all content under `course/day-01-*` through `course/day-05-*`
4. `LEARNING_GUIDE.md`
5. the relevant older `part-*` lab for the capability you are about to teach

Then verify the capability against **current official AWS AgentCore documentation**. Treat older `part-*` code as a reference, not as proof that an API, CLI command, model ID, or limitation is still current.

## Goal

Create the **next course day** using Days 1–5 as the quality bar.

The learner should be able to understand the concept without needing a trainer beside them.

## Mandatory teaching structure

The README must contain, in this order:

1. Today’s question
2. Why should I care?
3. One-sentence mental model
4. Build on yesterday
5. Architecture / request flow
6. Important terms
7. Read the code
8. Predict before running
9. Run it
10. Expected evidence
11. Break it on purpose
12. Learner assignment
13. Explain-back test
14. Production gap
15. Cleanup / cost hygiene
16. Next day

## Teaching constraints

- Introduce **one major new concept per day**.
- Keep the core example small and readable.
- Do not hide the AgentCore API being taught behind unnecessary abstractions.
- Prefer current common APIs over old model/provider-specific request formats.
- Use environment/configuration for ARNs, model IDs, Memory IDs, account IDs, secrets, and Regions.
- Do not hardcode real AWS resource IDs.
- Clearly separate responsibilities between:
  - client/backend,
  - AgentCore Runtime,
  - model provider/Bedrock Runtime,
  - AgentCore Memory,
  - Gateway/tools,
  - Identity,
  - other AgentCore services.
- Never describe Runtime process state as durable Memory.
- Define concrete expected evidence; "the command ran" is not enough.
- Include one deliberate failure experiment.
- Include a learner modification task.
- Include explain-back questions.
- State what is demo-grade versus production-grade.
- Include explicit cleanup/cost guidance for every AWS resource the lesson creates.

## Code constraints

- Target roughly 80–120 lines or less for the core teaching file where practical.
- Validate inputs at the application boundary.
- Use descriptive names.
- Avoid unnecessary classes/framework abstractions.
- Add comments only where they explain an AgentCore boundary or non-obvious behavior.
- Do not swallow errors in a way that prevents the learner from knowing which layer failed.
- Syntax-check modified Python files.

## Repository workflow

- Preserve existing work.
- Work on the existing course branch/PR unless instructed otherwise.
- Make small commits.
- Push each meaningful commit before starting the next change.
- Update `course/README.md` when a new day is added.
- Do not rewrite historical `part-*` labs merely to make them look like the course. Update them only when fixing a factual/correctness issue.

## Before declaring the day complete

Verify that a learner can answer:

- What problem does this new capability solve?
- Where does it sit in the request flow?
- What new API/resource was added today?
- What happens if that component fails?
- What evidence proves the behavior?
- What remains missing for production?

If those answers are not obvious from the README and code, improve the lesson before stopping.
