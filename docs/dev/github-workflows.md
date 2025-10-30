# GitHub Workflows

A workflow, as you may know, is just a set of instructions for completing a task.

As per usual in the world of software development, we like to take tasks, any task, and find the least-effort way of doing them.

GitHub workflows are an *automated* set of instructions for completing a task.

## A Yarn About YAML

Before I let you in on any details regarding the workflows, a short introduction to YAML is in order.

YAML, itself, stands for "YAML Ain't Markup Language". Yes, the acronym is itself part of its own acronym. While I wouldn't normally bring attention to the name of a language, it's worth keeping in mind how the acronym is *nested*.

---

Continuing with the standard introductions, you can, of course, give labels to data.

```yml
greeting: hello
goodbye: false
a_number: 10
```

And, just like the name, you can *nest* that data.

```yml
greeting:
  morning: Good morning
  afternoon: Good afternoon
  evening: Good evening
```

That's pretty much all we'll need to concern ourselves with. It's not meant to be complex. If you're looking for more, then have a look [here](https://learnxinyminutes.com/yaml/).

## Waltzing Workflows
