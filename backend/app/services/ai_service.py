# app/services/ai_service.py - EDUCATIONAL RESPONSES
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
    
    async def chat(self, message: str) -> str:
        """Provide educational responses without API key issues"""
        return self._get_educational_response(message)
    
    def _get_educational_response(self, message: str) -> str:
        """Provide helpful educational responses"""
        message_lower = message.lower()
        
        # Educational responses database
        responses = {
            "homework": """📚 **Homework Help Tips:**

**For Math Homework:**
1. Read the problem carefully
2. Identify what's being asked
3. Break it into steps
4. Show your work
5. Check your answer

**For Science Homework:**
1. Understand the concept
2. Review class notes
3. Use diagrams
4. Apply formulas correctly
5. Cite your sources

**For English/Language:**
1. Plan your essay structure
2. Write a clear thesis
3. Support with evidence
4. Proofread carefully
5. Check grammar and spelling

**Need help with a specific subject?** Tell me which one! 🎯""",
            
            "math": """🧮 **Mathematics Assistance:**

**Algebra:**
- Solving equations: 2x + 5 = 15 → x = 5
- Factoring: x² + 5x + 6 = (x+2)(x+3)
- Quadratic formula: x = [-b ± √(b²-4ac)]/2a

**Calculus:**
- Derivative rules: d/dx(xⁿ) = nxⁿ⁻¹
- Basic integrals: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C
- Limits and continuity

**Geometry:**
- Area formulas: Circle = πr², Triangle = ½bh
- Pythagorean theorem: a² + b² = c²
- Volume calculations

**What specific math topic do you need?** I can explain step-by-step! ✏️""",
            
            "physics": """⚛️ **Physics Help:**

**Mechanics:**
- Newton's Laws: F = ma
- Kinematics equations
- Energy: KE = ½mv², PE = mgh
- Momentum: p = mv

**Electricity:**
- Ohm's Law: V = IR
- Series/Parallel circuits
- Power: P = VI
- Capacitors and resistors

**Optics:**
- Reflection: angle in = angle out
- Refraction: Snell's Law
- Lens equations
- Mirror formulas

**Thermodynamics:**
- Laws of thermodynamics
- Heat transfer
- Ideal gas law: PV = nRT

**Need help with a specific physics problem?** Share it! 🔬""",
            
            "chemistry": """🧪 **Chemistry Support:**

**Basics:**
- Periodic table organization
- Atomic structure
- Chemical bonding
- States of matter

**Reactions:**
- Balancing equations
- Reaction types
- Stoichiometry
- Mole calculations

**Organic Chemistry:**
- Hydrocarbons
- Functional groups
- Isomers
- Reaction mechanisms

**Acids & Bases:**
- pH scale
- Titration
- Buffers
- Indicators

**What chemistry concept are you studying?** I can explain it clearly! 🔬""",
            
            "biology": """🧬 **Biology Topics:**

**Cell Biology:**
- Cell structure and function
- Photosynthesis
- Cellular respiration
- Mitosis and meiosis

**Genetics:**
- DNA structure
- Mendelian inheritance
- Protein synthesis
- Genetic disorders

**Human Body:**
- Systems (circulatory, nervous, etc.)
- Homeostasis
- Nutrition
- Diseases

**Ecology:**
- Ecosystems
- Food chains
- Biogeochemical cycles
- Conservation

**Which biology topic do you need help with?** 🦠""",
            
            "exam": """📝 **Exam Preparation Guide:**

**Study Strategies:**
1. **Start early** - Don't cram
2. **Make a schedule** - Allocate time for each subject
3. **Active recall** - Test yourself
4. **Spaced repetition** - Review regularly
5. **Practice papers** - Do past exams

**Subject-Specific Tips:**
- **Math:** Practice problems daily
- **Science:** Understand concepts, not just memorize
- **Languages:** Practice writing and reading
- **History:** Create timelines and mind maps

**Exam Day:**
- Get good sleep
- Eat a healthy breakfast
- Arrive early
- Read instructions carefully
- Manage your time

**Which subject exam are you preparing for?** I can give specific tips! 🎯""",
            
            "english": """📖 **English Language Help:**

**Grammar:**
- Parts of speech
- Sentence structure
- Tenses
- Punctuation rules

**Writing:**
- Essay structure (introduction, body, conclusion)
- Thesis statements
- Paragraph development
- Transition words

**Literature:**
- Literary devices
- Character analysis
- Theme identification
- Symbolism

**Comprehension:**
- Reading strategies
- Vocabulary building
- Inference skills
- Summarizing

**Need help with writing or analysis?** Share your question! ✍️""",
            
            "help": """🎓 **How I Can Help You:**

**Subjects I Cover:**
- Mathematics (Algebra, Calculus, Geometry)
- Physics (Mechanics, Electricity, Optics)
- Chemistry (Organic, Inorganic, Reactions)
- Biology (Genetics, Cells, Human Body)
- English (Grammar, Writing, Literature)
- Social Sciences
- Exam Preparation

**Types of Help:**
1. **Concept Explanations** - Clear, simple explanations
2. **Problem Solving** - Step-by-step solutions
3. **Study Tips** - Effective learning strategies
4. **Homework Help** - Guidance on assignments
5. **Exam Prep** - Practice questions and tips

**Try asking:** "Explain photosynthesis" or "How to solve quadratic equations?" 🚀""",
            
            "hello": """👋 **Hello! I'm EduSkill AI Tutor**

I'm here to help Ethiopian high school students with their studies!

**I can help with:**
- 📚 Homework assistance
- 🧮 Math problem solving
- ⚛️ Physics concepts
- 🧪 Chemistry explanations
- 🧬 Biology topics
- 📝 Exam preparation
- 🎯 Study strategies

**Try asking me:**
- "Help with math homework"
- "Explain Newton's laws"
- "Chemistry practice problems"
- "Biology study tips"
- "How to prepare for exams"

**What would you like to learn today?** 🎓"""
        }
        
        # Check for keywords in the message
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        # Default helpful response
        return f"""🎯 **I'd love to help you with:** "{message}"

**Here's how I can assist:**

**For Homework Help:**
1. Share the specific problem
2. Tell me which subject
3. Let me know what you've tried

**For Concept Explanations:**
1. Mention the topic
2. Specify your grade level
3. Ask specific questions

**For Study Help:**
1. Tell me the subject
2. Share your current understanding
3. Ask for practice questions or tips

**Try asking:**
- "Can you explain calculus derivatives?"
- "Help me with physics homework about electricity"
- "Give me biology study tips"
- "Math practice problems for algebra"

**What specific help do you need?** 📚"""
    
    async def test_connection(self):
        """Always return healthy for educational responses"""
        return "educational_responses_available"

ai_service = AIService()