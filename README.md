# Matchup-Level-ABS-Challenge-Value
Project Authors:
Jordan Gottlieb and Ryan Ilan

- Contact Information:
    - Jordan Gottlieb - gottlieb.jordan.d@gmail.com
    - Ryan Ilan - rilan270@gmail.com

- Personal GitHub Portfolios:
    - [Jordan Gottlieb](https://github.com/jdgott24)
    - [Ryan Ilan](https://github.com/rilan270)

- Project Description:
    - Our project researches the value of an ABS Challenge. We used machine learning, specifically an XGBoost model, to create a projection of RE288. We looked at data from the 2023-2025 seasons and compared it to the baseline standard RE288. Our model includes batter and pitcher statistics for their season-long performances to better estimate a player-specific run expectancy. Using this information, we created a strategy for how a team would use this in-game planning their approach to ABS. The model creates an RE288 table with projected numbers for a batter and pitcher matchup. It then calculates the value of a challenge for each of the 288 situations. Finally, the program calculates the confidence threshold needed to return zero run value. As a player, you would estimate your confidence the umpire was wrong. If your confidence is greater than the situation's confidence threshold, you would use your challenge. Our project also delivers an interpretable version of these charts for players and coaches to understand. Our decision matrix is the culmination of our research and explains what the value of a challenge is most dependent on. It is not reasonable to assume players can quantify their confidence in the short window after an umpire makes their call. Let alone, be able to remember all the possible matchups they might face and then the 288 situations for that specific matchup. The decision matrix is a simplified version of our charts that will guide players on our challenge strategy. In addition to the Decision Matrix, we would implement post-game audits following games. These will be held with players so that they will learn from their experience. The overall goal of this project is to improve how teams utilize ABS Challenges.

# How to use our Project:
- Please provide a citation, credit, or acknowledgement of our project if you are publicly sharing anything that was created using our work.
- Our project has a few features:
    - A matchup generator that will produce four charts:
        - A projected RE288 chart for the chosen matchup.
        - A chart showing the difference between actual observed RE288 and the projected RE288 for the chosen matchup.
        - A chart with the corresponding ABS challenge values for those 288 situations.
        - A chart showing the confidence value needed to use the challenge.
            - This value is also called the breakeven rate. If you challenge 100 times in a situation with a 30% confidence value and you are correct 30 times. You                 will net 0.0 runs from those challenges even though you were incorrect 70 times.
    - A probability calculator showing how often a situation with a higher run expectancy will occur after the current situation.
        - This is used to help understand challenge strategy throughout the course of a game.
