from .services import build_chat_messages, build_quick_prompt_links


def cultural_guide(request):
    history = request.session.get('guide_chat_history', [])
    latest_sources = []
    if history:
        latest_sources = history[-1].get('sources', []) or []

    return {
        'guide_chat_messages': build_chat_messages(history),
        'guide_quick_prompts': build_quick_prompt_links(),
        'guide_latest_sources': latest_sources,
    }