db_uri = "mongodb+srv://japmyy:bUGWHTwInFYJ" + "3kWK@cluster0.7eonw.mongodb.net/?r" + "etryWrites=true&w=majority&appName=Cluster0"
db_client = "dscapstrone"
db_collection = "userdata"


openai_api_key = "sk-proj-Xzh04" + "rXHHRmzJr4L6d4mYAtivOvAu-j8I5-v5Tan0" + "-6ndPqD-14aw84PYbVH_Gnx86Pwe9FctnT3BlbkFJQiJjPIbtrTn" + "LZdP0cxTYdPu_B82tpq3dEcMRoMWMqkNf1uzRLhg4P91OpdqNpz7VniVUgeFbwA" 


# Motivational messages
motivational_messages = [
    "Welcome to the app! Remember to do the exercise properly.",
    "You can do it! Stay focused and keep moving.",
    "Great to have you here! Every step counts.",
    "Believe in yourself! You are stronger than you think.",
    "Let's get moving! Your effort today leads to results tomorrow.",
    "Stay positive! Progress is progress, no matter how small.",
    "You've got this! Every moment is an opportunity to improve.",
    "Keep pushing your limits! Challenge yourself to do better.",
    "Success starts with the first step. Let’s take it together!",
    "Your journey is unique. Embrace every moment of it!",
    "Stay committed! Your hard work will pay off in the end.",
    "Great things take time. Keep at it, and you’ll see results!",
    "Remember, your only competition is yourself. Be the best you can be!",
    "Focus on the process, not just the results. Enjoy the journey!",
    "The only bad workout is the one that didn’t happen.",
    "Stay strong! Each day is a new chance to improve.",
    "Consistency is key. Keep showing up, and you will get there!",
    "Push through the tough times! They will make you stronger.",
    "Every drop of sweat brings you closer to your goals.",
    "Stay motivated! You are capable of achieving amazing things.",
    "Visualize your success! Picture yourself reaching your goals.",
    "Embrace the challenge! It’s what helps you grow.",
    "The journey may be tough, but so are you! Keep going.",
    "Celebrate your victories, no matter how small. They matter!",
    "Dedication and persistence lead to success. You’ve got this!",
    "Your body can stand almost anything. It’s your mind that you have to convince.",
    "You are not alone on this journey. We're in this together!",
    "Don’t just aim to be better than others; aim to be better than you were yesterday.",
    "Let your determination be stronger than your excuses.",
    "Stay committed to your goals, and the results will follow.",
    "Every day is an opportunity to improve yourself. Take it!",
    "You're making progress even on days when you feel like you’re not.",
    "Keep your head up and your heart strong. You're on the right path!",
    "You have the power to change your story. Start today!",
    "Believe in your abilities. You are capable of great things!",
    "Make today count! You won't get this day back.",
    "You are one workout away from a better mood. Let’s do this!",
    "Let’s crush those goals together! One step at a time.",
    "Your effort is a reflection of your dedication. Keep it up!",
    "Progress, not perfection, is the goal. Keep moving forward.",
    "Your mindset is everything. Choose positivity!",
    "Every rep counts, and every step brings you closer.",
    "Embrace the discomfort! It’s where the growth happens.",
    "Stay hungry for success! You are just getting started.",
    "You are stronger than your strongest excuse. Don’t let it win!",
    "Your potential is limitless! Keep striving for greatness.",
    "This is your moment! Own it and make the most of it.",
    "Success is the sum of small efforts repeated day in and day out."
]


body_parts = {
    "Head (Front)": (0, 0, 300, 100),
    "Left Shoulder (Front)": (50, 100, 150, 150),
    "Right Shoulder (Front)": (150, 100, 250, 150),
    "Chest": (75, 150, 225, 200),
    "Abdomen": (100, 200, 200, 300),
    "Left Arm (Front)": (0, 150, 75, 400),
    "Right Arm (Front)": (225, 150, 300, 400),
    "Hips": (100, 300, 200, 350),
    "Left Leg (Front)": (50, 350, 150, 587),
    "Right Leg (Front)": (150, 350, 250, 587),
    "Head (Back)": (310, 0, 500, 100),
    "Left Shoulder (Back)": (360, 100, 410, 150),
    "Right Shoulder (Back)": (450, 100, 500, 150),
    "Upper Back": (360, 150, 468, 180),
    "Middle Back": (370, 180, 468, 266),
    "Left Arm (Back)": (310, 150, 360, 400),
    "Right Arm (Back)": (500, 150, 550, 400),
    "Glutes": (360, 266, 475, 350),
    "Left Leg (Back)": (300, 350, 420, 587),
    "Right Leg (Back)": (420, 350, 550, 587)
}

exercise_recommendations = {
    "Head (Front)": ["Neck stretches", "Shoulder shrugs", "Head rotations"],
    "Left Shoulder (Front)": ["Shoulder rolls", "Arm circles", "Pendulum stretch"],
    "Right Shoulder (Front)": ["Shoulder rolls", "Arm circles", "Pendulum stretch"],
    "Chest": ["Chest stretch", "Arm pull stretch", "Wall push-ups"],
    "Abdomen": ["Pelvic tilts", "Seated knee lifts", "Core twist stretches"],
    "Left Arm (Front)": ["Wrist flexor stretch", "Bicep curls", "Arm stretches"],
    "Right Arm (Front)": ["Wrist flexor stretch", "Bicep curls", "Arm stretches"],
    "Hips": ["Hip flexor stretch", "Standing leg raises", "Knee-to-chest stretch"],
    "Left Leg (Front)": ["Quad stretch", "Calf raises", "Seated hamstring stretch"],
    "Right Leg (Front)": ["Quad stretch", "Calf raises", "Seated hamstring stretch"],
    "Head (Back)": ["Neck extensions", "Shoulder blade squeeze", "Head tilts"],
    "Left Shoulder (Back)": ["Shoulder blade squeeze", "Backward arm circles", "Scapula stretch"],
    "Right Shoulder (Back)": ["Shoulder blade squeeze", "Backward arm circles", "Scapula stretch"],
    "Upper Back": ["Cat-cow stretch", "Child's pose", "Thoracic extension"],
    "Middle Back": ["Seated twist", "Lat stretch", "Back rotations"],
    "Left Arm (Back)": ["Tricep stretches", "Wrist flexor stretch", "Arm circles"],
    "Right Arm (Back)": ["Tricep stretches", "Wrist flexor stretch", "Arm circles"],
    "Glutes": ["Pigeon stretch", "Seated figure-four stretch", "Glute bridges"],
    "Left Leg (Back)": ["Hamstring stretch", "Lunges", "Calf raises"],
    "Right Leg (Back)": ["Hamstring stretch", "Lunges", "Calf raises"]
}

