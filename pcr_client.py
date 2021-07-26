#!/usr/bin/env python3
'''PCR500MA client'''
from time import sleep

from ocs.matched_client import MatchedClient
from pcr500ma import VOLT_ULIM_TURNON, VOLT_ULIM_SOFT, PCRException

VOLT_STEP = 1
VOLT_ALLOW = 1
RAMP_TIME_STEP = 15


def ramp_simple(pcr_inst, volt, vstep=VOLT_STEP):
    '''Ramp to given voltage
    Parameters
    ----------
    pcr_inst : MatchedClient
        MatchedClient of PCR500MA.
    volt : float
        Target voltage in V.
    vstep : float, optional
        Voltage step for ramping.
    '''
    assert volt < VOLT_ULIM_SOFT, f'Target voltage exceeds {VOLT_ULIM_SOFT}V.'

    # Health check
    v_target_tmp = pcr_inst.get_volt_ac()
    _, _, s_meas = pcr_inst.meas()
    v_meas_tmp = s_meas['data']['v_ac']

    if abs(v_target_tmp - v_meas_tmp) > VOLT_ALLOW:
        raise PCRException(f'Discrepancy between taget and measured voltages: {v_target_tmp} / {v_meas_tmp}')

    # Voltage plan
    if v_target_tmp < volt:
        n_step = int((volt - v_target_tmp)/vstep)
        v_plan = [v_target_tmp + i*vstep for i in range(n_step)]
    elif v_target_tmp > volt:
        n_step = int((v_target_tmp - volt)/vstep)
        v_plan = [v_target_tmp - i*vstep for i in range(n_step)]

    v_plan = v_plan[1:] + [volt]

    for _v in v_plan:
        pcr_inst.set_volt_ac(volt_set=_v)
        sleep(0.5)
        _, _, s_meas = pcr_inst.meas()
        v_meas_tmp = s_meas['data']['v_ac']

        if abs(_v - v_meas_tmp) > VOLT_ALLOW:
            raise PCRException(f'Discrepancy between taget and measured voltages: {v_target_tmp} / {v_meas_tmp}')

        sleep(RAMP_TIME_STEP - 0.5)


def ramp_temp(pcr_inst, max_inst, volt):
    '''Ramp voltage 
    '''

def main():
    '''PCR client'''
    pcr_client = MatchedClient('stm-heater-source', args=[])

    pcr_client.set_volt_ac(volt_set=1)
    pcr_client.set_output(output=True)


if __name__ == '__main__':
    main()
