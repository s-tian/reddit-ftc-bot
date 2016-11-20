# reddit-ftc-bot
Automatically provides game rules for user reference.

Usage:
The bot responds to words of the form`'!' + rule_number` in comments in the specified subreddit with the full text of the rule from the FTC 2016-17 Game Manual Part 2. Multiple rules can be called for in the same comment. Letter casing and punctuation marks (`'`,`"`, `.`, `;`) do not prevent the bot from matching rules.

Example: `'!GS10, !S2, !G4 !gs15'` will result 

This project uses the PRAW (Python Reddit API Wrapper) and the OAuth2Util library. 

To install these libraries from pip, do `pip install praw` and `pip install praw-oauth2util`. 
In order to login to Reddit through OAuth2, you must set up a configuration file. See [this tutorial](https://github.com/SmBe19/praw-OAuth2Util/blob/master/OAuth2Util/README.md) for more information about using the OAuth2Util library.



