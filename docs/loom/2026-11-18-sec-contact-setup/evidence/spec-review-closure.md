# SEC contact setup — spec review closure

The independent spec review of 5003430 identified input-channel and wire-format gaps. The following are binding implementation constraints for the confirmed behavior.

- Use a dedicated non-echoing standard-input channel, with the command and contact payload passed separately. Shell literals, heredocs and echoed terminal input are excluded. If a host cannot supply that channel, report the setup failure without showing the values.
- Validate both fields and the final header before replacing the file. Preserve UTF-8 names by explicitly encoding the header at the HTTP boundary. A local Python reproduction verified that urllib accepts a bytes-valued header and http.client serializes it. Treat SEC acceptance of non-ASCII identity as an unverified network behavior.
- Distinguish absent configuration from inaccessible or corrupt configuration. The latter reports a repairable error without asking the user to repeat personal data. Preserve a usable prior file if replacement fails.
- Update both skill entry points and the current READMEs. Leave historical evidence in place.
- The client already rejects redirects. If a response reflects contact data, reject it before retaining raw bytes or computing an artifact from it. Do not silently rewrite a retained original.
