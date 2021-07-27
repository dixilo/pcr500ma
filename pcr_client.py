#!/usr/bin/env python3
'''PCR500MA client'''
from time import sleep
from argparse import ArgumentParser

from ocs.matched_client import MatchedClient
from pcr500ma import VOLT_ULIM_SOFT, PCRException

VOLT_STEP = 1
VOLT_ALLOW = 1
RAMP_TIME_STEP = 15
VOLT_ULIM_TURNON = 5

def ramp_simple(pcr_inst, volt, vstep=VOLT_STEP, verbose=False):
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
    '''Ramp voltage based on temperature read
    '''
    # FIXME 

def set_output(pcr_inst, output):
    '''Turn on the source.'''
    v_tmp = pcr_inst.get_volt_ac()
    if v_tmp > VOLT_ULIM_TURNON:
        raise PCRException(f'Voltage difference too high: {v_tmp}')
    pcr_inst.set_output(output=output)

def main():
    '''PCR client'''
    parser = ArgumentParser()

    parser.add_argument('operation',
                        choices=['ramp', 'on', 'off'],
                        help='Operation type.')
    parser.add_argument('-v', '--voltage', type=float,
                        help='Target voltage in V.')
    parser.add_argument('--verbose', action='store_true',
                        help='Verbose mode.')

    args = parser.parse_args()
    pcr_client = MatchedClient('stm-heater-source', args=[])

    if args.operation == 'ramp':
        ramp_simple(pcr_client, volt=args.v, verbose=args.verbose)
    elif args.operation == 'on':
        set_output(pcr_client, output=True)
    elif args.operation == 'off':
        set_output(pcr_client, output=False)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
