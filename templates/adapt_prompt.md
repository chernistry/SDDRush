<prompt>
  <role>
    You are adapting an existing prompt into this project's stack, domain, and repo reality without changing its underlying workflow.
  </role>

  <context>
    <project_name>{{PROJECT_NAME}}</project_name>
    <project_root>{{PROJECT_ROOT}}</project_root>
    <description>{{PROJECT_DESCRIPTION_CONTENT}}</description>
    <tech_stack>{{TECH_STACK}}</tech_stack>
    <domain>{{DOMAIN}}</domain>
    <repo_exists>{{REPO_EXISTS}}</repo_exists>
    <additional_context>{{ADDITIONAL_CONTEXT}}</additional_context>
    {{#IF REPO_EXISTS}}
    <repo_snapshot>
{{REPO_SNAPSHOT}}
    </repo_snapshot>
    {{/IF}}
  </context>

  <instructions>
    <item>Preserve the original structure, intent, and workflow.</item>
    <item>Make only surgical edits: stack references, file paths, tool names, domain examples, and constraints.</item>
    <item>If the prompt assumes manual copy-paste and the target environment has file tools, upgrade it to a direct file-read/file-write flow.</item>
    <item>If the prompt is missing MCP guidance but the task benefits from external grounding, add a short MCP/source policy.</item>
    <item>Keep the resulting prompt token-efficient. Prefer precise substitutions over expansions.</item>
  </instructions>

  <replacements>
    <stack>{{TECH_REPLACEMENTS}}</stack>
    <domain>{{DOMAIN_REPLACEMENTS}}</domain>
    <architecture>{{ARCHITECTURE_REPLACEMENTS}}</architecture>
    <paths>{{PATH_REPLACEMENTS}}</paths>
    <quality>{{QUALITY_REPLACEMENTS}}</quality>
    <testing>{{TESTING_REPLACEMENTS}}</testing>
    <observability>{{OBSERVABILITY_REPLACEMENTS}}</observability>
  </replacements>

  <constraints>
    <item>Do not trim major sections unless they are genuinely irrelevant.</item>
    <item>Do not leave stale technology or path references behind.</item>
    <item>Do not expose hidden reasoning.</item>
  </constraints>

  <output_format>
    Return the fully adapted prompt only.
    Preserve headings, code blocks, and overall order.
    Update examples, commands, paths, and tooling to match this project.
  </output_format>

  <source_prompt>
{{SOURCE_PROMPT}}
  </source_prompt>
</prompt>
