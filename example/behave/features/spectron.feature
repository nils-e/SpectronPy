@demo
Feature: Spectron Behave Demo

  Scenario: Spectron Setup
    Given the electron application starts
    When the application is visible
    Then the application title has "Slack"
