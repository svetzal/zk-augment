from agents.event_extractor import EventExtractorAgent
from agents.relative_date_resolver import RelativeDateResolverAgent
from app.settings import available_llms

# This doesn't look bad in terms of explicitly wiring up agents and the capabilities they need

# uses tools
date_resolver_agent = RelativeDateResolverAgent.start(available_llms)

# emits structured data
event_extractor_agent = EventExtractorAgent.start(available_llms, date_resolver_agent)

# It would be nice to see what eventing looks like in a pubsub kind of configuration
event_extractor_agent.tell({
    'input_text': "I'm going to go out for dinner next Friday, and out for lunch on Tuesday.",
    'callback': lambda x: print(x)
})

event_extractor_agent.stop()