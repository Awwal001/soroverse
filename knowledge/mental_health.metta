;; SOROverse Mental Health Knowledge Graph
;; Core Mental Health Ontology

;; Basic Emotions and States
(: emotion anxiety)
(: emotion depression)
(: emotion stress)
(: emotion joy)
(: emotion anger)
(: emotion fear)
(: emotion loneliness)

;; Cognitive Patterns
(: cognitive_pattern perfectionism)
(: cognitive_pattern catastrophizing)
(: cognitive_pattern black_white_thinking)
(: cognitive_pattern overgeneralization)
(: cognitive_pattern personalization)
(: cognitive_pattern mind_reading)

;; Coping Strategies
(: coping_strategy mindfulness_breathing)
(: coping_strategy journaling)
(: coping_strategy physical_exercise)
(: coping_strategy social_connection)
(: coping_strategy professional_help)
(: coping_strategy grounding_techniques)

;; Intervention Types
(: intervention_type CBT)
(: intervention_type DBT)
(: intervention_type mindfulness)
(: intervention_type exposure)
(: intervention_type acceptance)
(: intervention_type behavioral_activation)

;; Pattern Associations
(: association (perfectionism -> anxiety))
(: association (perfectionism -> stress))
(: association (catastrophizing -> anxiety))
(: association (catastrophizing -> depression))
(: association (black_white_thinking -> depression))
(: association (overgeneralization -> anxiety))
(: association (personalization -> anxiety))
(: association (mind_reading -> social_anxiety))

;; Intervention Effectiveness
(: intervention_effectiveness (CBT reduces anxiety 0.85))
(: intervention_effectiveness (CBT reduces depression 0.80))
(: intervention_effectiveness (mindfulness reduces stress 0.78))
(: intervention_effectiveness (DBT reduces emotional_dysregulation 0.82))
(: intervention_effectiveness (behavioral_activation reduces depression 0.75))

;; Crisis Indicators
(: crisis_indicator suicidal_ideation)
(: crisis_indicator self_harm_urges)
(: crisis_indicator severe_panic)
(: crisis_indicator dissociation)
(: crisis_indicator psychosis)

;; Crisis Protocols
(: crisis_protocol (suicidal_ideation -> immediate_human_support))
(: crisis_protocol (self_harm_urges -> crisis_helpline))
(: crisis_protocol (severe_panic -> grounding_techniques))
(: crisis_protocol (dissociation -> sensory_grounding))
(: crisis_protocol (psychosis -> emergency_services))

;; Peer Support Categories
(: peer_support_category academic_stress)
(: peer_support_category work_anxiety)
(: peer_support_category relationship_issues)
(: peer_support_category grief_loss)
(: peer_support_category life_transitions)

;; Session Types
(: session_type one_on_one)
(: session_type group_circle)
(: session_type workshop)
(: session_type check_in)