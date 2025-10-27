# 🧠 SOROverse: Decentralized Mental Wellness Network

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
![tag:mental-health](https://img.shields.io/badge/mental--health-FF6B6B)
![tag:peer-support](https://img.shields.io/badge/peer--support-4ECDC4)
![tag:wellness](https://img.shields.io/badge/wellness-96CEB4)
![tag:cognitive-mapping](https://img.shields.io/badge/cognitive--mapping-45B7D1)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![ASI Alliance](https://img.shields.io/badge/ASI-Alliance-blueviolet)

> **Where Empathy Evolves** - A decentralized mental wellness ecosystem combining self-awareness, community, and intelligent compassion.

## 🌟 Overview

**SOROverse** is a living ecosystem of autonomous AI agents that form a self-learning mental wellness network. It builds personalized digital twins of users' cognitive-emotional patterns, provides resilience-oriented companionship, and connects people through peer support communities - all powered by decentralized AI.

**Primary Audience**: Individuals seeking mental wellness support, emotional pattern understanding, and community connection through empathetic AI interactions.

## 💡 Use Case Examples

**Academic Stress Support**
- "I'm overwhelmed with exams and can't sleep" → Mindfulness exercises + study support groups
- "My perfectionism is causing burnout" → CBT techniques + peer validation

**Workplace Anxiety Management**
- "I'm stressed about upcoming presentations" → Breathing techniques + confidence building
- "Imposter syndrome is affecting my work" → Pattern recognition + peer mentorship

**Social Connection & Loneliness**
- "I feel isolated dealing with this challenge" → Peer matching + community circles
- "Need to talk to someone who understands" → Trained listener connections

**Personal Growth & Pattern Recognition**
- "Why do I keep feeling this way in relationships?" → Cognitive mapping insights
- "Want to understand my emotional triggers better" → Digital twin analysis

## 🔧 Capabilities

- **Real-time emotional pattern analysis** using MeTTa knowledge graphs
- **Evidence-based intervention selection** (CBT, mindfulness, reflection exercises)
- **Intelligent peer support matching** based on shared experiences and availability
- **Progressive cognitive mapping** of user's emotional landscape over time
- **Crisis detection and escalation protocols** with human backup
- **Community wisdom aggregation** through anonymized learning

## 💬 Interaction Modes

**Primary**: Direct messaging via ASI:One chat interface for personal support  
**Secondary**: Automated peer matching and group coordination  
**Background**: Continuous pattern learning and cognitive map updates  
**Future**: Webhook integrations with calendar and wellness applications

## ⚠️ Limitations

- Not a replacement for licensed therapists or emergency mental health services
- Effectiveness improves with consistent user interaction over time
- Peer matching capabilities depend on community participation and availability
- Currently optimized for English language interactions
- Requires user willingness to engage in self-reflection practices

---

## 🏗️ System Architecture

### Core Agents & Their Roles

| Agent | Address | Purpose |
|-------|---------|---------|
| **SoroMind Core** | `agent1q2w...` | Personal mental health companion and digital twin |
| **SOMA Engine** | `agent3e4r...` | Cognitive mapping and pattern reasoning |
| **SORO Orchestrator** | `agent5t6y...` | Intervention selection and delivery |
| **PSN Connect** | `agent7u8i...` | Peer support matching and community coordination |
| **MeTTa Query Engine** | `agent9o0p...` | Knowledge graph reasoning and insights |

### Input/Output Data Models

**Input Data Model**
```python
class MentalSupportRequest(Model):
    user_message: str
    emotion_context: Optional[str] = None
    support_type: Optional[str] = None  # 'immediate', 'reflection', 'peer'
```

**Output Data Model**
```python
class SupportResponse(Model):
    response_type: str  # 'reflection', 'intervention', 'peer_match', 'escalation'
    message: str
    suggested_actions: List[str]
    follow_up_questions: List[str]
```

### Technology Stack
- **Framework**: Fetch.ai uAgents
- **Deployment**: Agentverse
- **Knowledge**: SingularityNET MeTTa
- **Interface**: ASI:One via Chat Protocol
- **Compute**: CUDOS Network (analytics)
- **Storage**: Ocean Protocol (encrypted data)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- uAgents framework
- Agentverse account
- ASI:One access

### Installation
```bash
git clone https://github.com/your-username/soroverse
cd soroverse
pip install -r requirements.txt
```

### Running Locally
```bash
# Start the SoroMind Core agent
python agents/soromind_core.py

# Start the PSN Connect agent  
python agents/psn_connect.py
```

### Deployment to Agentverse
1. Register your agents on [Agentverse](https://agentverse.ai)
2. Enable Chat Protocol for each agent
3. Publish agent manifests
4. Test interaction via ASI:One

---

## 💬 How to Interact

### Via ASI:One
1. Open [ASI:One](https://asi.one) interface
2. Search for "SoroMind Core" agent
3. Start conversation: "I need mental health support"
4. Follow the empathetic conversational flow

### Example Interaction
```
User: "I've been really stressed preparing for exams. I can't sleep."

SoroMind: "That sounds exhausting. I notice this pattern of stress during exam periods. 
Would you like to:
1. Reflect on what's causing the stress?
2. Learn a quick relaxation technique?
3. Connect with others feeling similar pressure?"

User: "Option 2 please"

SoroMind: "Let's try a 3-minute mindfulness breathing exercise. 
Breathe in slowly... hold... and release. Notice how your body feels..."
```

---

## 🧩 Core Features

### 🪞 Personalized Digital Twin
- Learns your cognitive-emotional patterns over time
- Builds a MeTTa-based mind graph of your mental landscape
- Identifies triggers, coping mechanisms, and growth opportunities

### 💫 Proactive Resilience Building
- Predicts emotional downturns before they become critical
- Suggests evidence-based interventions (CBT, mindfulness, reflection)
- Tracks progress and adapts strategies based on effectiveness

### 🤝 Community Empowerment
- Matches you with trained peer supporters
- Facilitates group support circles based on shared experiences
- Builds mental health literacy through collective wisdom

### 🧠 Decentralized Knowledge Graph
- Evolving MeTTa graph of psychological patterns and interventions
- Privacy-preserving learning from anonymized community insights
- Evidence-based therapeutic protocols

---

## 🔧 Technical Implementation

### MeTTa Knowledge Graph Structure
```metta
;; Mental Health Ontology
(: emotion stress)
(: emotion anxiety)
(: emotion joy)
(: cognitive_pattern perfectionism)
(: cognitive_pattern catastrophizing)
(: coping_strategy mindfulness_breathing)
(: coping_strategy journaling)
(: coping_strategy peer_support)

;; Pattern Associations
(: association (perfectionism -> stress))
(: association (catastrophizing -> anxiety))
(: intervention (mindfulness_breathing reduces stress))
```

### Agent Communication Protocol
```python
class MentalStateAlert(Model):
    user_id: str
    risk_level: str  # 'low', 'medium', 'high', 'crisis'
    detected_patterns: list[str]
    recommended_actions: list[str]
    timestamp: datetime

class PeerMatchRequest(Model):
    user_id: str
    current_state: str
    preferred_support_type: str
    availability: list
```

---

## 📊 Demo Scenarios

### Scenario 1: Academic Stress Support
1. User reports exam stress and insomnia
2. SoroMind detects perfectionism pattern
3. SORO suggests mindfulness intervention
4. PSN Connect offers peer study group

### Scenario 2: Crisis Prevention  
1. User expresses overwhelming anxiety
2. System detects crisis indicators
3. Immediate escalation to human resources
4. Warm handoff with local support services

### Scenario 3: Community Growth
1. Long-term user becomes peer supporter
2. System recognizes developed empathy skills
3. PSN Connect trains and certifies as listener
4. User now supports others in community

---

## 🛡️ Privacy & Ethics

- **Data Sovereignty**: Users own their mental health data
- **Anonymization**: All community learning is anonymized
- **Consent**: Explicit opt-in for peer matching
- **Transparency**: Clear data usage policies
- **Crisis Protocols**: Immediate human escalation paths

---

## 🎯 Judging Criteria Alignment

| Criteria | How We Excel |
|----------|--------------|
| **Functionality (25%)** | Real-time multi-agent reasoning, crisis detection, community matching |
| **ASI Tech Usage (20%)** | Deep uAgents + MeTTa integration, Agentverse deployment, Chat Protocol |
| **Innovation (20%)** | Computational psychiatry + decentralized peer networks |
| **Real-World Impact (20%)** | Accessible mental health support, global scalability |
| **UX/Presentation (15%)** | Empathetic interactions, clear demo flow, comprehensive docs |

---

## 📁 Project Structure

```
soroverse/
├── agents/
│   ├── __init__.py
│   ├── soromind_core.py
│   ├── soma_engine.py
│   ├── soro_orchestrator.py
│   └── psn_connect.py
├── knowledge/
│   ├── __init__.py
│   ├── mental_health.metta
│   ├── interventions.metta
│   └── metta_manager.py
├── models/
│   ├── __init__.py
│   └── data_models.py
├── utils/
│   ├── __init__.py
│   ├── asi_client.py
│   └── crisis_detector.py
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_metta.py
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

---

## 🚀 Future Roadmap

- [ ] **Phase 1**: Core agent ecosystem (Current)
- [ ] **Phase 2**: Advanced pattern recognition
- [ ] **Phase 3**: Multi-language support
- [ ] **Phase 4**: Integration with wearable data
- [ ] **Phase 5**: DAO governance for community

---

## 👥 Team

- **Awwal** -  Lead & Agent Architecture
- **Zhulkurnein** - Project Coordinator

## 📞 Support

- **Discord**: [ASI Alliance Discord](https://discord.gg/asi-alliance)
- **Documentation**: [Agentverse Docs](https://docs.agentverse.ai)
- **Issues**: [GitHub Issues](https://github.com/awwal001/soroverse/issues)

---

## 📜 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **ASI Alliance** for the incredible infrastructure
- **Fetch.ai Innovation Lab** for uAgents framework
- **SingularityNET** for MeTTa knowledge graphs
- All the mental health professionals who informed our approach

---

> **"Healing is not a solitary journey. In SOROverse, we grow together, learn together, and heal together."**

**Start your journey at: [Agentverse - SoroMind Core](https://agentverse.ai)**
