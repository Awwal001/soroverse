;; Detailed Intervention Protocols

;; Mindfulness Interventions
(: intervention (mindfulness_breathing 
    (: technique "4-7-8 Breathing")
    (: steps 
        "Breathe in through nose for 4 seconds"
        "Hold breath for 7 seconds" 
        "Exhale through mouth for 8 seconds"
        "Repeat 4 times")
    (: duration_minutes 5)
    (: effectiveness_anxiety 0.82)
    (: effectiveness_stress 0.85)))

(: intervention (body_scan_meditation
    (: technique "Progressive Body Scan")
    (: steps
        "Lie down comfortably"
        "Focus attention on toes, notice sensations"
        "Slowly move attention up through body parts"
        "Spend 20-30 seconds on each area"
        "Notice without judgment")
    (: duration_minutes 10)
    (: effectiveness_stress 0.78)
    (: effectiveness_sleep 0.80)))

;; CBT Interventions
(: intervention (thought_challenging
    (: technique "Cognitive Restructuring")
    (: steps
        "Identify automatic negative thought"
        "Examine evidence for and against thought"
        "Consider alternative perspectives"
        "Develop balanced thought")
    (: duration_minutes 15)
    (: effectiveness_depression 0.75)
    (: effectiveness_anxiety 0.80)))

(: intervention (behavioral_experiment
    (: technique "Testing Beliefs Through Action")
    (: steps
        "Identify prediction or belief"
        "Design small experiment to test it"
        "Carry out experiment safely"
        "Record actual outcomes vs predictions")
    (: duration_minutes 20)
    (: effectiveness_anxiety 0.70)))

;; DBT Interventions
(: intervention (distress_tolerance
    (: technique "ACCEPTS")
    (: steps
        "Activities: engage in distracting activities"
        "Contributing: help someone else"
        "Comparisons: put situation in perspective"
        "Emotions: generate different emotions"
        "Pushing away: temporarily block thoughts"
        "Thoughts: replace thoughts"
        "Sensations: intense physical sensations")
    (: duration_minutes 10)
    (: effectiveness_crisis 0.85)))

;; Crisis Interventions
(: intervention (crisis_grounding
    (: technique "5-4-3-2-1 Sensory Grounding")
    (: steps
        "Name 5 things you can see"
        "Name 4 things you can touch"
        "Name 3 things you can hear"
        "Name 2 things you can smell"
        "Name 1 thing you can taste")
    (: duration_minutes 3)
    (: effectiveness_panic 0.88)))

;; Social Interventions
(: intervention (social_connection_plan
    (: technique "Structured Social Engagement")
    (: steps
        "Identify 2-3 supportive people"
        "Schedule brief check-ins"
        "Practice sharing feelings"
        "Set boundaries as needed")
    (: duration_minutes 30)
    (: effectiveness_loneliness 0.75)))