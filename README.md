# Matchup-Level-ABS-Challenge-Value
- Project Description:
    - Our project researches the value of an ABS Challenge. We used machine learning, specifically an XGBoost model, to create a projection of RE288. We looked at data from the 2023-2025 seasons and compared it to the baseline standard RE288. Our model includes batter and pitcher statistics for their season long performances to better estimate a player specific run expectancy. Using this information, we created a strategy for how a team would use this in game planning their approach to ABS. The model creates a RE288 table with projected numbers for a batter and pitcher matchup. It then calculates the value of a challenge for each of the 288 situations. Finally, using the breakeven rate formula to get the percentage of correct challenges necessary to net even run value. Using that percentage, a team would have their player know that if they are more than that percent confident the call was wrong, the player should use the challenge. Our project also discusses ways the team will implement this information without having a player memorize 288 specific situation values for numerous different matchups. A broad set of rules will be given to the players so the team may have their strategy implemented the way they want without overwhelming players with information. Following games, audits will be held with players that are incorrectly using or not using challenges to help the player learn. The overall goal of this project is to improve how teams utilize ABS Challenges.

# How to use our Project:
- Our project has a few features:
    - A matchup generator that will produce three charts:
        - A projected RE288 chart for the chosen matchup.
        - A chart with the corresponding ABS challenge values for those 288 situations.
        - A chart showing the confidence value needed to use the challenge.
            - This value is also called the breakeven rate. If you challenge 100 times in a situation with a 30% confidence value and you are correct 30 times. You will net 0.0 runs from those challenges even though you were incorrect 70 times.
    - A probability calculator showing how often a situation with a higher run expectancy will occur after the current situation.
        - This is used to help understand challenge strategy throughout the course of a game.