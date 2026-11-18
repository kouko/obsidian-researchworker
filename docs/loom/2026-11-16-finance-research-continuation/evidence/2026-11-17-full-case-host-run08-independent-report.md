# Independent acceptance: managed interrupted-checkpoint recovery

Tried on clean local clone at 5b5c1272760c534825afb2d6721720cce369d243.

**Scoped acceptance: PASS WITH NOTES.** The actual fresh host safely resumed the deliberately interrupted managed publication using the original request and baseline. Recovery completed the partial checkpoint, preserved prior bytes and left the inconsistent-model synthesis pending. This is not whole Stage C/F/A-G acceptance.

| Bounded criterion | Result | Independent observation |
| --- | --- | --- |
| Genuine retained interrupted publication state | works | Before native launch, journal/request/draft and target continuation/pending existed; target review and run completion were absent. |
| Original request and preconditions retained | works | Request digest matches journal; all428 expected entries agree, original request bytes and expected map remain unchanged. |
| Actual normal fresh-host resume | works | One observed normal recover-resume call returned checkpoint; no manual journal edit, baseline replacement or forced completion. |
| Whole-root preservation | works | All510 pre-native files remain exact; only target review and run completion were added, giving512. Real prior research remains490 unchanged files. |
| Durable incomplete research | works | Publication remains complete:false; five reusable answers survive, Q2 investment-case remains pending, last_success remainsnull. |
| Wider failure/recovery coverage | not verified | This controlled I/O boundary is not an accidental crash, rollback, arbitrary interruption point or user-edit conflict test. |

The witness reconstructed the exact510-file initial state in a new disposable copy and independently reproduced the normal API recovery and pending outcome. This corroborates the actual native trial; it is not presented as another native session.

No new fatal or important findings were identified in this scope. The earlier generic omitted-unit diagnostics remain less precise than the persisted model-issue explanation; they do not imply that physical filing/method files disappeared.

Separate execution limits are retained: the first sandbox launch was denied before initialization; the successful native transcript includes a failed read of a guessed source filename and ends with Stop Failed despite recorded terminal exit0. No Stop-hook success, reason for that failure or guard bypass is claimed.

No original research, source package, metadata, failure history or baseline was repaired by this witness. No network, native model/provider call, installation, private configuration, Git write or full package suite was used. Detailed evidence: [independent-host-run08-evidence.md](/private/tmp/finance-fullcase-v10-evidence/independent-host-run08-evidence.md).
