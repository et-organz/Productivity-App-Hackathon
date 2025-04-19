# Focus +

**Focus +** is a Pomodoro-based study system designed to boost your focus and maximize learning retention. Backed by the latest research in cognitive science and productivity, this tool helps you structure your study sessions for optimal performance.

## Features

- 🕒 Pomodoro Timer: Stay focused with customizable Pomodoro intervals.
- 📚 Science-Backed: Built on proven techniques to enhance memory retention.
- 🎯 Goal-Oriented Sessions: Track your progress and stay motivated.
- 🛠️ Lightweight & Easy to Use: Clean interface that gets out of your way.

## Why It Works

The Pomodoro Technique leverages focused work sprints followed by short breaks. This approach improves concentration and reduces mental fatigue. By integrating this with research-backed learning strategies, **Focus +** helps you study smarter, not harder.

## Getting Started

Clone the repo and install the requirements:

```bash
git clone https://github.com/et-organz/Productivity-App-Hackathon
cd Productivity-App-Hackathon
pip install -r requirements.txt
touch .env
```
Make sure to add a ChatGPT api key to the .env file under OPENAI_API_KEY

## Blocking Websites
### How to use the Website Blocking 

Select *Add Website*
![Blocking](assets/blocking-home-screen.png)

Enter your website URL
![Add Blocking](assets/website-url.png)

### How to remove a Website

Highlight a website and then click on *Remove Website*
![Blocked Websites](assets/added-blocks.png)

Website removed
![Website Removed](assets/website-removed.png)

# How to use Pomodoro
![Pomodoro View](assets/Pomodoro.png)

Click *Settings* and enter in desired work duration, short-break duration, and long-break duration. 

![Work Duration](assets/work-duration.png)
![Short-Break Duration](assets/short%20duration.png)
![Long-Break Duration](assets/long%20duration.png)

Finally, click *Start* to begin the timer

# Break Apps

### Doodling 
Doodling until your hearts content. Pressing *Enter* on the keyboard toggles constant drawing - no need to hold onto the mouse! Pressing *Space* enters Etch A Sketch mode allowing you to relieve your childhood. 
![Doodling](assets/doodling.png
)

### Learn Prompt
Enter what you would like to be tested on, and the LLM will create test questions for your to answer!
![learn-prompt](assets/learn-prompt.png)

### Box Breathing
Follow the prompts for a destressing session!
![Box Breathing](assets/box-breathing.png)

### Reflection Prompt
State what you learned during your study session. The LLM will generate some questions for you to think about. 
![Reflection](assets/reflection.png)

# Website Tracking and Test Question Generator 
Please note that this only works with Google Chrome
![Website Main](assets/webmain.png)

## Web Tracking
Click *Start Tracking* and watch as the websites you have visited in Google Chrome are added to a visited website list. Click *Stop Tracking* to stop tracking your visited websites. 
![Tracking List](assets/tracking-list.png)

## Test Question Generator
Click *Continue* to begin selecting websites to generate questions from. Select the links that you would like to be quizzed on and click *Submit* to generate the prompt (This make tame some time).

![Select Links](assets/select-links.png)

### Answer the Questions
Answer the questions and click *Submit Answer*. Results may take some time to appear.
![Questions](assets/questions-gen.png)

### Feedback
The LLM will generate feedback based on how you answered the question. 

![Feedback](assets/feedback.png)

