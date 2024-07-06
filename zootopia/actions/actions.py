# problem: we need a simple abstraction module that takes us from a certain interaction
# to a certain result; luckily, most actions for now are expected to be in text form

# idea:
# build a simple way to break down all action logic

# literally all you have to define are define 'action-blocks' which are:
# - intent:
#       a description of the parameters data needs to meet in order for action to run
# - action:
#       what will happen with that data


# example:
# user gave their name:
# -> update that in the database
# user asks a question about something
# -> query it and answer
# user asks for the weather
# -> use the weather api
# user is trying to jailbreak
# -> ping moderator

# NOTES:
# there should be pre and post actions, actions that will run pre/post all action-blocks

#########################
# LLM Generated Examples (all within logical scope of our solution):
#########################

# User wants to translate text
# -> Detect language, translate, and provide pronunciation guide

# User uploads an image
# -> Analyze image content, generate tags, and suggest similar images

# User inputs a song title
# -> Find lyrics, chord progression, and suggest covers/remixes

# User provides symptoms
# -> Suggest possible conditions and recommend specialist types

# User inputs a recipe
# -> Calculate nutritional information and suggest ingredient substitutions

# User shares their location
# -> Provide local events, air quality data, and sunset/sunrise times

# User inputs a math problem
# -> Solve the problem and generate a step-by-step explanation

# User provides a writing prompt
# -> Generate a short story and suggest similar literary works

# User inputs a product name
# -> Compare prices across platforms and provide review summaries

# User shares their mood
# -> Suggest mood-appropriate music, activities, and self-care tips

# User inputs a coding question
# -> Provide code snippet, explain logic, and suggest best practices

# User shares travel dates and destination
# -> Provide packing list, local customs info, and currency exchange rates

# User inputs a debate topic
# -> Present arguments for both sides and suggest credible sources

# User shares their workout routine
# -> Analyze for muscle group balance and suggest complementary exercises

# User inputs a historical event
# -> Provide timeline, key figures, and long-term impacts


# define a chain of what happens, through configs...

# you get a message
# what do you do with it?
# build action blocks to connect 2 things together

# what this will look like:
# "action-chain" - a list of intents and its associating actions
# each action can also contain an action-chain
