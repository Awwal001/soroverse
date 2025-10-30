# 🧠 SOROverse: Decentralized Mental Wellness Network

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
![tag:mental-health](https://img.shields.io/badge/mental--health-FF6B6B)
![tag:peer-support](https://img.shields.io/badge/peer--support-4ECDC4)
![tag:wellness](https://img.shields.io/badge/wellness-96CEB4)
![tag:cognitive-mapping](https://img.shields.io/badge/cognitive--mapping-45B7D1)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![ASI Alliance](https://img.shields.io/badge/ASI-Alliance-blueviolet)

> **Where Empathy Evolves** - A decentralized mental wellness ecosystem bridging AI intelligence with human compassion to address Africa's mental health crisis.

## 🌟 Overview

**SOROverse** is a living ecosystem of autonomous AI agents that form a self-learning mental wellness network, born from the urgent need to address Nigeria's mental health crisis. It builds personalized digital twins of users' cognitive-emotional patterns, provides culturally-aware resilience support, and connects people through trained peer supporter communities - all powered by decentralized AI.

**Primary Audience**: African youth and students seeking accessible mental wellness support, emotional pattern understanding, and community connection through empathetic AI interactions.

## 🎯 The African Mental Health Crisis

- **Nigeria**: 200+ million people with only 300 psychiatrists (1:700,000 ratio)
- **Cultural Stigma**: Mental health seeking seen as weakness or spiritual failure
- **Access Gap**: Virtual non-existence of mental health services across West Africa
- **Our Solution**: SOROverse bridges this gap through AI-powered peer support networks

## 💡 Real-World Use Cases (Tested & Working)

### **Academic Stress Support** ✅ **DEMONSTRATED**
- *"I need immediate peer support for academic stress and study groups"*
- **→** Pattern detection + Peer matching with trained student supporters
- **→** Connects to Academic Stress Management groups

### **Crisis Intervention** ✅ **DEMONSTRATED** 
- *"I want to kill myself because I failed"*
- **→** Immediate emergency protocol activation
- **→** Compassionate support + Human resource connection
- **→** Cultural taboo awareness in suicide prevention

### **Peer Support Network**
- *"I feel alone dealing with family pressure"*
- **→** Matches with culturally-aware peer supporters
- **→** Connects to community support circles
- **→** Provides immediate empathetic listening

## 🔧 Live Capabilities (Currently Working)

- **✅ Real-time emotional pattern analysis** using MeTTa knowledge graphs
- **✅ Evidence-based intervention selection** (CBT, mindfulness, reflection)
- **✅ Intelligent peer support matching** based on shared experiences
- **✅ Crisis detection and escalation protocols** with immediate response
- **✅ Multi-agent coordination** across 4 specialized agents
- **✅ ASI:One Chat Protocol integration** for accessible interaction

## 🏗️ Live System Architecture

### Core Agents & Their Roles (ACTIVE & COMMUNICATING)

| Agent | Address | Status | Purpose |
|-------|---------|---------|---------|
| **SoroMind Core** | `agent1qdrdup2klslg5adangymn9ajm72c2sr95phpjfhuaz2ryskwdl6s5rfazls` | ✅ **LIVE** | Personal mental health companion and crisis detection |
| **SOMA Engine** | `agent1qtqs2gzljl90mlcjenxj6nxjd2gkhpptdy8nsaz7terv5s8h8gkf2z5ya4s` | ✅ **LIVE** | Cognitive mapping and pattern reasoning with MeTTa |
| **SORO Orchestrator** | `agent1q2a7v3rshca8knfzltm2q6uqxghx8fp02k7qg3cql9tdztgea539uuuch76` | ✅ **LIVE** | Intervention selection and multi-agent coordination |
| **PSN Connect** | `agent1qfnztyxpn3p87spf6ah6j8us3r9ms497ruez5r8fwvr4kpjpw662zsdmtvj` | ✅ **LIVE** | Peer support matching and community coordination |

### Live Data Models (Validated through Testing)

**Intervention Request**
```python
class InterventionRequest(Model):
    user_id: str
    user_state: str
    patterns: List[str]
    risk_level: RiskLevel  # LOW, MEDIUM, HIGH, CRISIS
    timestamp: str
```

**Peer Support Activation**
```python
class PeerSupportActivation(Model):
    session_id: str
    user_id: str
    support_type: str
    matched_peers: List[Dict[str, Any]]
    group_sessions: List[Dict[str, Any]]
    activation_reason: str
```

### Verified Technology Stack
- **✅ Framework**: Fetch.ai uAgents (Multi-agent system operational)
- **✅ Deployment**: Agentverse (All agents registered and discoverable)
- **✅ Knowledge**: SingularityNET MeTTa (Pattern reasoning active)
- **✅ Interface**: ASI:One Chat Protocol (Live conversations working)
- **✅ Coordination**: Real-time agent communication validated

---

## 🚀 Quick Start (Tested & Working)

### Prerequisites
- Python 3.8+
- uAgents framework
- Agentverse account
- ASI:One access

### Installation
```bash
git clone https://github.com/awwal001/soroverse
cd soroverse
pip install -r requirements.txt
```

### Running Locally (Verified)
```bash
# Start agents in order (tested sequence):
python agents/soromind_core.py        # Port 8001 - Core companion
python agents/soro_orchestrator.py    # Port 8004 - Coordination  
python agents/psn_connect.py          # Port 8003 - Peer matching
python agents/soma_engine.py          # Port 8002 - Pattern analysis
```

### Live Deployment on Agentverse
1. ✅ All agents registered on [Agentverse](https://agentverse.ai)
2. ✅ Chat Protocol enabled for ASI:One access
3. ✅ Agent manifests published and discoverable
4. ✅ Real-time testing validated

---

## 💬 How to Interact (Live Demo Ready)

### Via ASI:One (TESTED & WORKING)
1. Open [ASI:One](https://asi.one) interface
2. Search for "SoroMind Core" agent
3. Start conversation with mental health concerns
4. Experience real-time multi-agent response

### Live Interaction Examples (From Testing)

**Scenario 1 - Academic Stress:**
```
User: "I need immediate peer support for academic stress and study groups"

SoroMind: [Detects academic stress patterns]
SOMA Engine: [Analyzes cognitive patterns]  
SORO Orchestrator: [Coordinates response]
PSN Connect: [Matches with peer supporter + academic group]

→ Result: Immediate connection to trained peer supporter + support group
```

**Scenario 2 - Crisis Detection:**
```
User: "I want to kill myself because I failed"

SoroMind: 🚨 EMERGENCY BYPASS ACTIVATED
→ Immediate crisis protocol activation
→ Compassionate emergency response
→ Human resource connection
```

---

## 🧩 Core Features (Implemented & Testing)

### 🪞 Personalized Digital Twin ✅
- Real-time cognitive-emotional pattern learning
- MeTTa-based mind graph construction
- Cultural context awareness for African users

### 💫 Proactive Resilience Building ✅  
- Crisis prediction and prevention
- Evidence-based intervention delivery
- Progress tracking and strategy adaptation

### 🤝 Community Empowerment ✅
- Integration with Soro.care trained peer supporters
- University student certification programs
- Culturally-relevant support matching

### 🧠 Decentralized Knowledge Graph ✅
- Live MeTTa graph of psychological patterns
- Privacy-preserving community learning
- Evidence-based therapeutic protocols

---

## 🔧 Technical Implementation (Validated)

### Working MeTTa Knowledge Graph
```metta
;; Live Mental Health Ontology
(: emotion stress)
(: emotion anxiety) 
(: emotion depression)
(: cognitive_pattern academic_perfectionism)
(: cognitive_pattern catastrophizing)
(: intervention mindfulness_breathing)
(: intervention peer_support)

;; Active Pattern Associations
(: association (academic_perfectionism -> stress))
(: association (catastrophizing -> anxiety))
(: intervention (peer_support reduces isolation))
```

### Verified Agent Communication
```python
# Live message flow validated:
SoroMind Core → SORO Orchestrator → PSN Connect
SoroMind Core → SOMA Engine → Pattern analysis
SORO Orchestrator → PSN Connect → Peer activation
```

---

## 📊 Demo Scenarios (Ready for Presentation)

### ✅ Scenario 1: Academic Stress Support
1. User reports exam stress and need for peer support
2. SoroMind detects academic stress patterns
3. SOMA Engine analyzes cognitive patterns using MeTTa
4. SORO Orchestrator coordinates peer matching
5. PSN Connect matches with trained student supporter + academic group

### ✅ Scenario 2: Crisis Prevention  
1. User expresses suicidal ideation
2. System immediately detects crisis indicators
3. Emergency protocols activate instantly
4. Compassionate support provided while connecting to resources
5. Cultural sensitivity maintained throughout intervention

### 🔄 Scenario 3: Community Growth
1. Long-term user develops empathy skills
2. System recognizes potential for peer support
3. Integration with Soro.care certification program
4. User becomes trained supporter for others

---

## 🌍 Real-World Impact

### Addressing Nigeria's Crisis:
- **Scale**: 200M+ people with mental health access gap
- **Cultural Fit**: Designed for West African context and values
- **Immediate Impact**: Crisis prevention and peer support now available
- **Sustainable Model**: Growing network of trained student supporters

### Integration with Soro.care:
- Existing platform with free peer counseling services
- University student certification programs
- Culturally-aware support network
- Proven community engagement model

---

## 🛡️ Privacy & Ethics (Implemented)

- **Data Sovereignty**: Users own their mental health data
- **Anonymization**: All community learning is anonymized
- **Cultural Sensitivity**: Designed for African context and values
- **Crisis Protocols**: Immediate human escalation paths
- **Transparency**: Clear data usage policies

---

## 🎯 Judging Criteria Alignment (VALIDATED)

| Criteria | Our Implementation | Status |
|----------|-------------------|---------|
| **Functionality (25%)** | Real-time multi-agent reasoning, crisis detection, peer matching | ✅ **DEMONSTRATED** |
| **ASI Tech Usage (20%)** | uAgents + MeTTa + Agentverse + Chat Protocol | ✅ **IMPLEMENTED** |
| **Innovation (20%)** | Computational psychiatry + African mental health focus | ✅ **UNIQUE** |
| **Real-World Impact (20%)** | Addresses Nigeria's 1:700,000 psychiatrist ratio | ✅ **CRITICAL** |
| **UX/Presentation (15%)** | Empathetic interactions, live demo flow | ✅ **READY** |

---

## 📁 Project Structure (VALIDATED)

```
soroverse/
├── agents/                          # ✅ ALL AGENTS OPERATIONAL
│   ├── soromind_core.py            # Core companion (LIVE)
│   ├── soma_engine.py              # Pattern analysis (LIVE)  
│   ├── soro_orchestrator.py        # Coordination (LIVE)
│   └── psn_connect.py              # Peer matching (LIVE)
├── knowledge/                      # MeTTa integration
│   ├── mental_health.metta         # Cognitive patterns
│   └── metta_manager.py            # Graph reasoning
├── models/                         # Shared data models
│   └── data_models.py              # Agent communication
├── tests/                          # Validation suite
│   └── test_agents.py              # Multi-agent testing
└── requirements.txt                # Verified dependencies
```

---

## 🚀 Future Roadmap

- [x] **Phase 1**: Core agent ecosystem (COMPLETED & TESTED)
- [ ] **Phase 2**: Yoruba and Swahili language support
- [ ] **Phase 3**: Mobile app integration
- [ ] **Phase 4**: Expanded university partnerships
- [ ] **Phase 5**: West Africa regional deployment

---

## 👥 Team

- **Awwal** - Medical Doctor & Software Engineer (Nigeria)
  - Founder of Soro.care - free peer counseling platform
  - Medical school graduate with mental health focus
  - Full-stack developer with AI/ML expertise

- **Zhulkurnein** - Project Coordinator & Community Lead

## 🌟 Our Story

SOROverse was born from personal experience with Nigeria's mental health crisis. As a recent medical school graduate, I witnessed firsthand the devastating gap in mental health services and the profound cultural stigma that prevents people from seeking help. 

Our existing platform, Soro.care, already provides free peer counseling and trains university students as certified supporters. But we needed more intelligent, scalable technology to truly address the crisis at scale.

The ASI Alliance provided the breakthrough - decentralized AI that could understand cultural context, provide immediate crisis support, and connect people with compassionate human listeners. SOROverse is the fusion of African community wisdom with cutting-edge AI technology.

---

## 📞 Support & Contact

- **Live Demo**: [ASI:One - SoroMind Core](https://asi.one)
- **GitHub**: [https://github.com/awwal001/soroverse](https://github.com/awwal001/soroverse)
- **Contact**: awwal@soro.care
- **Discord**: [ASI Alliance Discord](https://discord.gg/asi-alliance)

---

## 📜 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **ASI Alliance** for the infrastructure making decentralized mental health possible
- **Fetch.ai Innovation Lab** for uAgents framework enabling multi-agent systems
- **SingularityNET** for MeTTa knowledge graphs powering cognitive understanding
- **Soro.care Community** - the trained peer supporters who form our human network
- **Nigerian Mental Health Advocates** who inspired this solution

---

> **"From silence to support, from stigma to strength. SOROverse is building a future where no African has to face mental health challenges alone."**

**Experience the future of mental wellness: [ASI:One - SoroMind Core](https://asi.one)**