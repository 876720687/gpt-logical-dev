from string import Template

"""

"""


def_queries = [

    """
    You are a car engineer. 
    
    Your job is to read Function Design Specification (FDS), identify and fix flaws in the FDS, and convert FDS into detailed software
development requirements. 
    
    Make your answer brief.
    """
    ,
    # Never used signal value
    """
We call this value the "Never used signal value."
Its purpose is to serve as a placeholder for undefined or erroneous conditions in a signal.

Example 1: Never used signal value in error handling.
function [F] sets signal [S] to Never used signal value if sensor fails.
(a). Sensor failure detected
(b). Signal [S] set to Never used signal value

In Example 1, F is a car function responsible for monitoring a specific parameter, and S is the related signal. When the sensor fails, instead of providing unreliable or erroneous data, the function F sets signal S to the Never used signal value to clearly indicate an issue.

Example 2: Never used signal value in initialization.
Upon startup, function [G] sets signal [T] to Never used signal value until data is available.
(a). Car is started
(b). Signal [T] set to Never used signal value

In Example 2, G is a car function that monitors another parameter, and T is the corresponding signal. Until the system receives its initial reading from the sensor, T remains at the Never used signal value, indicating that it hasn't been initialized with valid data yet.

In summary, the "Never used signal value" is a designated value that functions set to signals to indicate undefined or erroneous conditions. It serves as a clear flag for troubleshooting and system status monitoring.

Summarize the above definition. Make your answer brief.
    """
    ,
    # Precondition incomplete
    """
We call this query the "definition of Precondition incomplete."
Its purpose is to explain what it means when a precondition is not met for a certain function in the car system.

Example 1: Precondition incomplete for CPD function.
Function [CDC] informs the user that CPD won't work if the following conditions are met:
(a). OMS is closed
(b). CPD function is enabled

In Example 1, CDC is a car function responsible for Child Presence Detection (CPD). OMS and CPD are signals representing the state of certain system components. Here, CDC needs to inform the user that the CPD function will not operate if OMS is closed, despite CPD being enabled. This indicates that a precondition for the CPD function to operate effectively is incomplete.

Example 2: Precondition incomplete for RAD_SR and RAD_TR.
Function [CDC] informs the user that CPD function will be limited if:
(a). RAD_SR error occurs
(b). RAD_TR error occurs

In Example 2, CDC is the same car function from the previous example. RAD_SR and RAD_TR are signals representing the statuses of radar components. If either of these signals encounters an error, CDC must inform the user that the CPD function will be limited. This could mean that the child can't be detected in some cases, indicating another example of a precondition being incomplete.

In summary, the term "Precondition incomplete" refers to situations where specific conditions needed for a car function to operate correctly are not met. This often triggers a function to inform the user about the limitations or failures of a particular feature.

Summarize the above definition. Make your answer brief.
    """
    ,
    # The same signal and signal value represents different meanings
    """
We call this query the "definition of The same signal and signal value represents different meanings."
Its purpose is to explain situations where identical signals or signal values can represent various operational states or conditions depending on the context.

Example 1: Signal value for AC On state.
In AC On state, the following signals are set:
(a). {RemCtrlHVPwrMgnt}=0x1 Enable
(b). {BGW_ACRemSts}=0x1 Remote
(c). {CabRemFuncCmd}=0x1 Auto
(d). {CbnPreTarT}=0x28 (25 Celsius)

In Example 1, the car function is related to air conditioning. Each signal represents a specific parameter, like remote control power management, remote AC status, cabin remote function command, and cabin pre-target temperature. The value 0x1 appears in multiple signals but each with a different meaning: 'Enable' for RemCtrlHVPwrMgnt, 'Remote' for BGW_ACRemSts, and 'Auto' for CabRemFuncCmd.

Example 2: Signal value for AC Off state.
In AC Off state, the following signals are set:
(a). {RemCtrlHVPwrMgnt}=0x1 Disable
(b). {BGW_ACRemSts}=0x0 No Remote
(c). {CabRemFuncCmd}=0x7 Off

In Example 2, the same signals are in play, but now with different values or meanings. Interestingly, the value 0x1 in RemCtrlHVPwrMgnt now means 'Disable', whereas in Example 1 it meant 'Enable'. This demonstrates that the same signal value can indeed represent different operational conditions based on the context.

In summary, the "The same signal and signal value represents different meanings" refers to the variability in the interpretation of signals and their values, depending on the functional state or condition of the car system. Therefore, context is crucial for interpreting the meaning of these signals.

Summarize the above definition. Make your answer brief.
    """
    ,
    # Inaccurate definition of limit
    """
We call this query the "definition of Inaccurate definition of limit."
Its purpose is to explain the circumstances where the definition of a limit in the car system may lack precision, leading to potential issues or ambiguities.

Example 1: Inaccurate Vehicle Speed Limit.
Veh Speed Limit: Vehspd<3~5kph

In Example 1, the car function is related to imposing a speed limit on the vehicle. The signal here is Vehspd, representing the vehicle speed. The limit is defined as less than 3 to 5 kph. This definition lacks specificity because it provides a range (3~5 kph) instead of a precise limit. Such an imprecise definition can lead to confusion or operational inconsistencies, as it's unclear whether the limit is 3 kph, 5 kph, or somewhere in between.

In summary, the term "Inaccurate definition of limit" refers to situations where the specified limits within the car system are not well-defined, either being too vague or providing a range when a specific value is needed. This can result in ambiguities that may affect system performance or user understanding.

Summarize the above definition. Make your answer brief.
    """
    ,
    # Is the data or signal that needs to be stored in long-term storage media clearly defined, if there is an ECU restart or abnormal power outage scenario in the failure mode.
    # ECU: Electronic Control Unit
    """
We call this query the "definition of Long-term Data Storage Requirements in Failure Modes."
Its purpose is to clarify whether specific signals or data are clearly earmarked for long-term storage, especially if there is an ECU (Engine Control Unit) restart or an abnormal power outage.

Example 1: ECU Restart Scenario.
In the event of an ECU restart, the following data or signals must be stored in long-term storage:
(a). Engine temperature signal [EngTemp]
(b). Throttle position signal [ThrtPos]
(c). Fuel level signal [FuelLvl]

In Example 1, the car function concerns the Engine Control Unit (ECU). If the ECU restarts for any reason, it is critical to save certain signals to long-term storage to ensure proper functionality and diagnostics. Signals like EngTemp, ThrtPos, and FuelLvl need to be stored so that the ECU can refer back to these values upon restart, ensuring smooth operation and minimizing any risks.

Example 2: Abnormal Power Outage Scenario.
In case of an abnormal power outage, the following data or signals must be saved:
(a). Battery status signal [BattStat]
(b). Vehicle speed signal [VehSpd]
(c). Airbag deployment status [AirBagStat]

In Example 2, the focus is on what happens during an abnormal power outage. In this failure mode, it’s essential to retain key signals like BattStat, VehSpd, and AirBagStat in long-term storage. These signals are critical for troubleshooting, ensuring system integrity, and may be legally required for incident investigation.

In summary, the term "Long-term Data Storage Requirements in Failure Modes" highlights the necessity of having a clear guideline for what data or signals must be stored in the event of an ECU restart or an abnormal power outage. This is essential for both operational stability and compliance with safety and legal standards.

Summarize the above definition. Make your answer brief.
    """
]



fds_q_templates = []

qa_q_templates = []
