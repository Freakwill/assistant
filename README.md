# assistant
An extensible expert system.

## Assistant
assistant = parser + inference engine + database
parser: parse your question
inference engine: fine the answer
database: store the knowledge

## Controler
Control the conversation between you and assistants.

## Commands
`c.register_command('len', lambda x, y: print(len(y)))`
where x is an assistant, y is the history of your questions.

## How to do it?
```python
import assistant

with assistant.Controler() as c:
    c.register_command('len', lambda x, y: print(len(y)))
    sa = assistant.SimpleAssistant.create('Lisa')
    c.run(sa)
```
Following is the conversation.

    Welcome, my host.
    [New assistant Lisa is created]
    -- I am Lisa, Can I help you? (input [q]uit to quit)
    --
    -- What is your question?
    -- How to do it?
    -- I don't know.[last time:Thu Dec 27 11:24:46 2018]
    -- Are you satisfied with the answer?[Press enter for yes] If not, show the right answer.
    -- Fuck it!
    -- What is your question?
    -- How to do it?
    -- Fuck it![last time:Thu Dec 27 11:24:52 2018]
    -- Are you satisfied with the answer?[Press enter for yes] If not, show the right answer.
    --
    -- ^_^
    -- What is your question?
    -- %reset
    -- What is your question?
    -- How to do it?
    -- I don't know.[last time:Thu Dec 27 11:25:31 2018]
    -- Are you satisfied with the answer?[Press enter for yes] If not, show the right answer.
    -- Screw it!
    -- What is your question?
    -- How to do it?
    -- Screw it![last time:Thu Dec 27 11:25:48 2018]
    -- Are you satisfied with the answer?[Press enter for yes] If not, show the right answer.
    --
    -- ^_^
    -- What is your question?
    -- quit
    -- Goodbye.
    Do you want to save the new data?[y/n]y
    data are saved.
    The controler is shut down.
