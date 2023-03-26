Feature: Schedule
    An API that can tell you the amount of seconds until a job is executed

    Scenario: Getting the time until a job is executed
        Given I scheduled a job

        When I make a GET call to the timer API

        Then I should get the estimated time until execution
