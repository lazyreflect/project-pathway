# Best Practices for Crafting Commands for Agent-D

Agent-D is a powerful tool designed to automate web interactions, including secure login processes on various websites. To achieve a high success rate when sending commands to the Agent, it's crucial to craft clear, precise, and detailed instructions. This document provides guidelines and examples to help you formulate effective commands.

## Guidelines for Generating Effective Commands

### 1. Be Specific with Actions and Websites

- **Specify the exact website URL** you want the Agent to navigate to.
- **Clearly state the action** you want the Agent to perform (e.g., "log in", "navigate to", "press the button").

### 2. Anticipate and Describe Potential Redirects or Prompts

- If the website might redirect to a different page or display prompts (like a login button), **include these possibilities in your command**.
- Mention any **additional steps** that may be required after the initial action.

### 3. Include Conditional Instructions

- Use conditional statements to handle scenarios where additional input or actions may be needed.
- For example: "If you are told an email with a verification code was sent, enter the code."

### 4. Define Clear Termination Conditions

- Indicate when the Agent should terminate the task, especially if an action cannot be completed.
- Provide instructions on **reporting errors** or specific messages if the task fails.

### 5. Reference Specific Page Elements

- When necessary, **identify specific buttons, fields, or sections** by their names or labels.
- This helps the Agent locate and interact with the correct elements on the page.

### 6. Use Numbered Steps for Complex Tasks

- For tasks involving multiple steps, **break down instructions into numbered lists**.
- This ensures the Agent follows the intended sequence of actions accurately.

## Examples

Below are examples extracted and adapted from successful test cases to illustrate how to apply these best practices.

### Example 1: Simple Login

**Command:**

```
Go to emomed.com and log in using the enter secret credentials tool. If you cannot log in the first time, terminate and report the error message.
```

**Explanation:**

- Clearly states the target website (`emomed.com`) and the action (`log in` using a specific tool).
- Provides a termination condition if the login is unsuccessful.

### Example 2: Login with Conditional Verification

**Command:**

```
Go to providers.dentaquest.com and log in. Then, if you are told an email with a verification code was sent, enter the code. If you cannot log in the first time, terminate and report the error message.
```

**Explanation:**

- Anticipates an additional step (entering a verification code) and includes it conditionally.
- Maintains clarity on what to do if the login fails.

### Example 3: Navigating Through Redirections

**Command:**

```
Your goal is to navigate to https://app.dentalhub.com/app/dashboard. If you are redirected to a page with a button that says login, press the button. Then, log in. If you cannot log in the first time, terminate and report the error message.
```

**Explanation:**

- Mentions the possibility of a redirection and instructs the Agent on how to handle it.
- Specifies the exact button to press ("button that says login") before proceeding to log in.

### Example 4: Accepting License Agreements

**Command:**

```
Go to https://www.cyberaccessonline.net/ and log in. Then, you may be redirected to a page that will have you read a license agreement, then press a button that says 'I Agree'. Press the button. Then wait for the final loading screen to load. If you cannot log in the first time, terminate and report the error message.
```

**Explanation:**

- Anticipates an intermediate step (accepting a license agreement) and provides specific instructions.
- Ensures the Agent waits for the final screen, indicating awareness of loading times.

### Example 5: Complex Task with Multiple Steps

**Command:**

```
1. Navigate to the URL https://comfortdentalsid.curvehero.com/#/.
2. Check if redirected to a login page.
3. If on a login page, log in.
4. Verify successful login or capture any error message if login fails.
5. Identify the name input field, then input the name 'Mike Lee'.
6. If more than one patient named Mike Lee is found, select the one without a DOB.
7. Click on the 'Insurance' button.
8. Identify the insurance plan that Mike Lee has.
```

**Explanation:**

- Breaks down a complex task into numbered steps for clarity.
- Includes conditional logic to handle multiple patients with the same name.
- Specifies exact field names and actions to guide the Agent precisely.

## Additional Tips

- **Use Clear and Concise Language:** Avoid ambiguity by using straightforward language.
- **Avoid Overloading Commands:** Keep commands focused; if a task is too complex, consider breaking it into smaller subtasks.
- **Test Commands Individually:** Before deploying, test each command to ensure it performs as expected.
- **Update for Website Changes:** Websites may update their interfaces; ensure your commands reflect the current site structure.

## Conclusion

By following these best practices, you can craft commands that enable Agent-D to perform tasks accurately and efficiently. Clear, precise instructions help the Agent understand your intent and reduce the likelihood of errors. Always consider potential variations in website behavior and provide the Agent with the necessary information to handle them.
