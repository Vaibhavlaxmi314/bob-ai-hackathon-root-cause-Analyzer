"""
watsonx.ai Granite inference wrapper.
Set WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL in .env for real calls.
Without a real key the module falls back to STUB mode — returns deterministic
mock responses so all other code paths can be tested without credentials.
"""
import os

_STUB = not bool(os.getenv("WATSONX_API_KEY", "").strip().replace("your_api_key_here", ""))

if not _STUB:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference

    _model = ModelInference(
        model_id="ibm/granite-13b-instruct-v2",
        credentials=Credentials(
            api_key=os.getenv("WATSONX_API_KEY"),
            url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
        ),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={"max_new_tokens": 512, "temperature": 0.2},
    )


def generate(prompt: str) -> str:
    """Send prompt to Granite and return the response text."""
    if _STUB:
        return _stub_response(prompt)
    return _model.generate_text(prompt=prompt)


# ---------------------------------------------------------------------------
# Stub responses — realistic enough to validate UI and API contracts
# ---------------------------------------------------------------------------
def _stub_response(prompt: str) -> str:
    p = prompt.lower()

    if "rerouting" in p or "alternative" in p or "carrier" in p:
        return (
            "RECOMMENDATION 1: Reroute via Cape of Good Hope using CMA CGM (carrier). "
            "Estimated additional delay: 12 days. Cost differential: +18%. "
            "Reasoning: Avoids disrupted region entirely with confirmed vessel availability.\n"
            "RECOMMENDATION 2: Air freight transfer to Frankfurt hub using Lufthansa Cargo. "
            "Estimated additional delay: 2 days. Cost differential: +340%. "
            "Reasoning: Fastest option for high-priority or time-critical cargo.\n"
            "RECOMMENDATION 3: Hold at origin port and rebook next available slot. "
            "Estimated additional delay: 4-6 days. Cost differential: +5%. "
            "Reasoning: Lowest cost option if delivery deadline allows flexibility."
        )

    if "temperature" in p or "excursion" in p or "cold chain" in p or "severity" in p:
        if "16" in p or "13" in p or "critical" in p:
            return (
                "SEVERITY: CRITICAL. "
                "The recorded temperature significantly exceeds the safe maximum for this cargo type. "
                "Prolonged exposure at this level will result in irreversible spoilage. "
                "ACTION: Quarantine shipment immediately upon arrival. Do not distribute. "
                "Initiate regulatory incident report. Contact shipper and consignee within 2 hours."
            )
        if "11" in p or "10" in p or "reportable" in p:
            return (
                "SEVERITY: REPORTABLE BREACH. "
                "Temperature exceeded the safe range for a sustained period. "
                "Product integrity may be compromised. Laboratory testing required before release. "
                "ACTION: Flag shipment for quality hold on arrival. Notify cold chain compliance officer. "
                "Document excursion duration and peak temperature for regulatory dossier."
            )
        return (
            "SEVERITY: MINOR DEVIATION. "
            "Temperature briefly exceeded the safe range but returned within limits. "
            "Risk of spoilage is low for most cargo types at this deviation level. "
            "ACTION: Document the excursion in the shipment record. "
            "Conduct visual inspection on arrival. No hold required unless deviation repeats."
        )

    return "Analysis complete. No specific recommendation pattern matched — review input context."
