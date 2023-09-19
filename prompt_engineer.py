from string import Template

######## new concept definations ########
def_queries = [
    '''
You are a car engineer. Your job is to read Function Design Specification (FDS),
identify and fix flaws in the FDS, and convert FDS into detailed software 
development requirements. Make your answer brief.
''',

    '''
We call this query the "definition of signal expression".
Its purpose is to explain what is a signal expression.
Following are two examples.

Example 1: signal expression that has only one result signal.
function [F] sets signal [S] as value positive if expression a&b
(a). signal [X] is 1 
(b). signal [Y] is 0

In Example 1, F is a car function. S, X and Y are all signals.
S is the only one "result signal", because the purpose of this 
signal expression is to assign values to S. S will be set as 
positive if X is 1 and Y is 0.

Example 2: signal expression that does not have a result signal.
function [F] will enter [M] mode if signal [S] is positive.

In Example 2, F is a car function. S is a signal.
M is a working mode that F is in when S is positive.
This signal expression does not have any "result signal",
because the purpose of this signal expression is not to
assign any value to any signal.

Summarize the above definition. Make your answer brief.
''',

    '''
We call this query the "definition of signal expression group".
Its purpose is to explain how to group signal expressions.

The signal expressions of the same group should satisfy three conditions:

First, signal expressions of the same group should be controled 
by the same function. 

Second, all signal expressions of the same group should have
the same result signal. Note that there is only one result signal 
for a signal expression group.


Third, a signal expression group must have at least two signal expressions. 

Following is an example.

Expression1:
function [F] sets signal [S] as value 4 if expression a&b
(a). signal [X] is 1 
(b). signal [Y] is 0

Expression2:
function [F] sets signal [S] as value 3 if expression a||b
(a). signal [X] is 0 
(b). signal [Y] is 1

Expression3:
function [F] sets signal [Z] as value 2 if expression a&&b
(a). signal [X] is 1 
(b). signal [S] is 0

Expression4:
function [E] sets signal [S] as value 4 if expression a&&b
(a). signal [X] is 1 
(b). signal [S] is 0

Expression5:
function [F] shall enter mode [M] if signal [S] is 4.

In this example, F is a car function. S, X, Y and Z are all signals.
Expression1 says: function F will set result signal S as 4 if signal X is 1 and signal Y is 0.
Expression2 says: function F will set result signal S as 3 if signal X is 0 and signal Y is 1.
Expression3 says: function F will set result signal Z as 2 if signal X is 1 and signal S is 0.
Expression4 says: function E will set result signal S as 4 if signal X is 1 and signal Y is 0.
Expression5 says: function F will enter mode M if signal S is 4.

Expression1 and Expression2 are grouped as one signal expression group
because they satisfy the three conditions.

Expression3 does not belong to this group because signal Z is different 
from result signal S and thus violates the second condition.

Expression4 does not belong to this group because function E is different 
from function F and thus violates the first condition.

Expression5 does not belong to any group because this expression does
not have a result signal.

Expression2 and Expression3 are not considered as one group because
Expression2's result signal S and Expression3's result signal Z
are different.

Summarize the above definition. Make your answer brief.
''',

    '''
We call this query the "definition of timer".
Its purpose is to explain timer operations.

Operation 1:
Start. This operation starts the timer to count down.
We also use "trigger", "enable" and other similar words 
to represent this operation.

Operation 2:
Expire. This operation means the timer has been counted 
down to 0. We also use "stop", "is expired" and other
similar words to represent this operation.

Operation 3:
Stop. This operation means the timer stops counting down
before it expires. The timer remains what is left in the time
counter. We also use "halt", "hold" and other
similar words to represent this operation.

Operation 4:
Reset. This operation means we stop the current timer before
it expires and reset the timer to its initial value. 

Operation 5:
Reload. This operation means Start after Reset. In other words,
we stop the timer before it expires, reset the timer to its 
initial value, and start the timer counting down.

As a timer, Start, Expire and Reset are the 3 basic operation
that must be defined.

Summarize the above definition. Make your answer brief.
''',

    '''
We call this query the "definition of single signal 
expression mistake". Its purpose is to describe mistakes
that are usaully seen in a single signal expression.

Mistake 1:
Timer that does not reset. Use the timer operations defined 
in "definition of timer" to understand this mistake.
FDS should explicitly explain if resetting timer is necessary 
in three places: after the timer expires, after the timer stops, 
before the timer starts. This mistake may cuase a misbehaved 
timer and trap the system in a never-defined status.

Mistake 2:
Timeout without followup actions. FDS needs to explicitly
define what to do after a timer times out. When timeout happens,
the system could transit to a well-defined state or could
trigger an error handling process. However, it is a mistake
if the FDS does not define what to do after a timer times out.

Summarize the above definition. Make your answer brief.
''',

    '''
We call this query the "definition of signal expression 
group mistake". Its purpose is to describe mistakes
that are usaully seen in a signal expression group.
A signal expression group is defined in 
"definition of signal expression group".

Mistake 1:
Multiple signal expressions simultaneously satisfied.
In this mistake, more than one signal expressions
of the same signal expression group can be all
satisfied at the same time. 

Mistake 2:
None of signal expressions satisfied. In this mistake, 
All signal expressions of the same signal expression group 
are not satisfied at the same time. 

Summarize the above definition. Make your answer brief.
''',
]



######## template to query pdf file ########
fds_q_templates = [
    Template('''
We call this query and its answer the "documented signal expressions".
Its purpose is to identify all the signal expression texts 
in chapter $chapter.

Identify all the original texts that contains signals. Do not cutoff, 
rewrite or interpret. We call these texts the 
"original signal expressions".
    '''),

    Template('''
We call this query and its answer the "documented signals".
Its purpose is to identify all the signals in chapter $chapter.
A signal usually has three characteristic:

First, a signal must have multiple possible values. Note that 
a signal and a signal value are two different concepts. 
For example, signal S can be ON or OFF. 
In this case, S is a signal, while ON and OFF are signal values. 
Do not classify a signal value as a signal.

Second, a function or function block is a component that assigns
values to signals. For example, function F assigns signal S to ON,
in which F stands for a function, S stands for a signal and
ON stands for a signal value. As a result, a function or function 
block is not a signal. Do not classify a function or function block 
as a signal.

Third, a signal's name cannot be found in a dictionary. Instead, it is 
in the form of multiple abbreviations. For example, signal "VehState" 
stands for "vehicle state". Note that "_", "-" and other forms 
of connecting symboles may be used in a signal's name as well.

Return a dictionary. The dictionary key is the signal name. 
The dictionary value is all the possible values of the
corresponding signal. Do not interpret each individual signal. 
Do not say anything else.
    '''),
]

######## template to query chatgpt ########
qa_q_templates = [
    Template(
        '''
We call this query and its answer the "qa of signal expression groups".
Its purpose is to group the signal expressions in
the "original signal expressions" defined in "documented signal expressions".
Do following step by step.

Step 1, for each of the signal expression of the original signal expressions,
identify if it is a signal expression that has a result signal
or it is a signal expression that does not have a result signal. 
For signal expression that has a result signal, hight light its function and 
result signal. Organize the output in four columns: 
signal expression index, function, has result signal or not, result signal.

Step 2, Group the signal expressoins in the "original signal expressions" 
according to the "definition of signal expression group".

Note that the signal expressoins of the same group must 
follow three conditions: they are controlled by the same function, 
they have only one and the same result signal, a group must contain 
at least two signal expressions.

Ignore the signal expressoin that does not have a result signal, 
Do not put it into any group.

Ignore the group that contains only one signal expressoin.

Organize the output as following format:
Group index, signal expression index, function, result signal, signal expression

We call these groups the "original signal expression groups".
'''),

    Template('''
We call this query and its answer the "qa of signal expression mistakes".
Its purpose is to identify all the signal expression mistakes in
the "original signal expressions" defined in "documented signal expressions". 
Do following step by step.

Step 1, use the "definition of single signal expression mistake" 
to identify the mistakes in each of the expressions in the 
"original signal expressions".

Step 2, use the "definition of signal expression group mistake" 
to identify the mistakes in the "original signal expression groups"
defined in "qa of signal expression groups". For each of the mistakes,
explicitly list the signal expressions and the signal values 
that cause this mistake. Try to give fixes to resolve the mistake. 
'''),
]