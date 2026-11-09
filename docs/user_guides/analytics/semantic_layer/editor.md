---
description: How to edit the YAML definitions of a semantic project in the Hopsworks UI, with validation as you type, saves that never overwrite another edit, and when the editor is read only.
---

# Edit Definitions in the UI { #semantic-editor }

The definitions editor opens the YAML files of a semantic project in the browser, validates them as you type, and saves them to the project's file system.
Open the semantic project from **Semantic Layer** in the project sidebar and click **Edit definitions**, or click the file of an issue in a build's issues on the **Builds** card, which opens the editor at its line.

## Edit and validate { #semantic-editor-edit }

The editor lists the `.yml` and `.yaml` files under the semantic project's root path, the files a compile reads, read anew each time the editor opens.

- Pick a file in the tree to open it; a changed file is marked in the tree until it is saved, and so is a file with errors.
- **New file** asks for a path under the root path, such as `models/orders.yml`; the file is created when you save it.
- Half a second after you stop typing, Hopsworks validates the files as they are in the editor, saved and unsaved, as a compile would, and stores nothing.
  The status next to the name reads **Validating**, **Valid**, **Valid, 2 warnings**, or the count of errors and warnings, such as **1 error**, **Validation busy, retrying** when the Hopsworks instance runs two validations already, or **Validation unavailable** when the validation fails; the next edit validates again.
  Each issue is underlined at its line in the editor and listed under **Validation**, with its rule and message as in [Validation rules][semantic-validation-rules]; clicking an issue's file opens it at its line.
- **Save** writes the open file.
  A save does not compile: click **Compile**, or let a later query's staleness check compile it, see [When a compile runs][semantic-builds-triggers].
- **Overview** goes back to the semantic project's page.
- With unsaved changes, leaving the editor for another page asks first: **Stay** keeps the edits, **Discard and leave** drops them.
  Closing or reloading the browser tab asks the browser's own question.
- Changing the root path, format or repository in **Edit** opens the definitions from the new source, and drops the unsaved edits of the old one.

A file holds at most 1 MiB, and the root path at most 1,000 definition files and 32 MiB, as for a compile.
A path must end in `.yml` or `.yaml` and stay under the root path; symbolic links are refused.
Files are read and written as you, so HopsFS permissions apply as in the file browser, and a saved file keeps its permissions.

## Saves never overwrite another edit { #semantic-editor-conflicts }

A save names the version of the file it was opened at.
When someone saved the file after you opened it, in the editor or anywhere else, the save is refused, and the editor shows **The file changed since you opened it** with **Reload**, which opens their version and discards your edits to that file.
Two saves of one file from the editor at the same moment are serialised, and the second is refused, even from two semantic projects whose root paths share the file.
A write outside the editor, from the file browser, Jupyter, a terminal or git, does not wait for an editor save in progress.

## Read only { #semantic-editor-read-only }

The editor shows the files and their issues without **Save** and **New file**, with the reason under **Read only**, when:

| Case | Reason shown |
| --- | --- |
| The semantic project is in a Hopsworks git repository | The definitions are in a git repository. Change them there and pull, which compiles them. |
| The semantic project is compiled from a `semantic_manifest.json` | dbt generates the manifest. Change the dbt project and generate the manifest again. |
| You cannot write to the root path in HopsFS | You cannot write to the folder that holds the definitions. |
| Your role in the project cannot change semantic projects | Only Data Owners and Data Scientists change semantic projects. |

## Over REST { #semantic-editor-rest }

The editor's endpoints are under `/hopsworks-api/api/project/<project id>/semantic/projects/<semantic project id>/`, for Data Owners and Data Scientists; an API key needs the `FEATURESTORE` scope.

| Method | Path | Does |
| --- | --- | --- |
| GET | `files` | `{"files": [{"path", "size", "etag"}], "readOnly", "readOnlyReason"}`, the reason `GIT`, `JSON` or `ROLE`. |
| GET | `files/<path>` | The file's text, with its `ETag`, the sha256 of its bytes. |
| PUT | `files/<path>` | Saves the body: with `If-Match: <etag>` it replaces that version, with `If-None-Match: *` it creates the file. Answers 200 with the new `ETag`. |
| DELETE | `files/<path>` | Deletes the file, with `If-Match: <etag>`. Answers 204. |
| POST | `validate` | Validates the stored files with `files` laid over them, a path to its text, or to `null` for a deleted file. |

```bash
curl -X POST -H "Authorization: ApiKey $HOPSWORKS_API_KEY" -H "Content-Type: application/json" \
  -d '{"revision": 17, "files": {"models/semantic.yml": "semantic_models:\n  - name: orders\n    model: ref('"'"'orderz'"'"')\n"}}' \
  "https://hopsworks.example.com/hopsworks-api/api/project/119/semantic/projects/7/validate"
```

```json
{
  "revision": 17,
  "status": "INVALID",
  "errorCount": 1,
  "warningCount": 0,
  "issues": [
    {"level": "ERROR", "rule": "RELATION", "message": "no feature group in demo_featurestore matches orderz", "file": "models/semantic.yml", "line": 2, "column": 5, "element": "semantic_model:orders"}
  ]
}
```

`revision` comes back as sent, so a client can drop the answer to an older buffer.

| Error | Code | Status | Meaning |
| --- | --- | --- | --- |
| `SEMANTIC_LAYER_FILE_NOT_FOUND` | 590060 | 404 | The file does not exist. |
| `SEMANTIC_LAYER_FILE_CHANGED` | 590061 | 412 | The file is not the version `If-Match` names, or exists for an `If-None-Match: *`. |
| `SEMANTIC_LAYER_PRECONDITION_REQUIRED` | 590062 | 428 | A save without `If-Match` or `If-None-Match: *`. |
| `SEMANTIC_LAYER_READ_ONLY` | 590063 | 409 | The semantic project is in a git repository, or compiled from a `semantic_manifest.json`. |
| `SEMANTIC_LAYER_VALIDATION_BUSY` | 590064 | 429 | The Hopsworks instance runs two validations already; try again shortly. |
