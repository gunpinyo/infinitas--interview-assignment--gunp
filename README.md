# infinitas--interview-assignment--gunp
This repository contains the assignment (for Gun Pinyo)
as an interview preparation for Infinitas (by Krungthai).

Note: to ensure the reproducibility, we will encapsulates
the whole assignment using Docker (see `.Dockerfile`).

Note: to ensure the confidentiality, we will put all secret in `secret.yaml`,
which only exists locally. I will attach this secret file in the submission
email.

# Task 1: LINE Notify

The solution is in [`src/task_1.py`](src/task_1.py).

![images/line-notify-testing-result.jpg](images/line-notify-testing-result.jpg)

Since the provided access-token can't be used for testing purpose, so I create
my own access-token especially for testing.
![images/line-access-token.png](images/line-access-token.png)

Both tokens are stored in `secret.yaml`. In this case, we can treat the provided
token as the token for production environment whereas my own token is for
development. Therefore, I have a variable `line-access-token-key` in
`config.yaml` to quickly change the environment.

![images/pip-line-outdate.png](images/pip-line-outdate.png)

Lastly, I notice that pip package `line_notify` was released on 27 Dec 2017 (5
years ago) so this package might be outdate. Nevertheless, I stick with this
package because it is the most popular among alternative package. In real case
scenario, I suggest that we directly manage the restful API which is publicized
in <https://notify-bot.line.me/doc/en/>.

