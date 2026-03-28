# Automated Testing with AI

How to generate and run tests using the agent.

## Generation
Inside Aider or VS Code Chat:
- "Write unit tests for [file.js] using Vitest."
- "Create an integration test for the API endpoint."

## Execution
1. Ask the agent to create a test script: "Add a test script to package.json."
2. Run tests locally: `npm test` or `pytest`.
3. If tests fail: Copy output to agent and say "Fix code to pass these tests."
