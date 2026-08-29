export enum ReturnRequestStatus {
  SUBMITTED = 'SUBMITTED',
  APPROVED = 'APPROVED',
  RETURN_LABEL_SENT = 'RETURN_LABEL_SENT',
  PACKAGE_RECEIVED = 'PACKAGE_RECEIVED',
  INSPECTION_PASSED = 'INSPECTION_PASSED',
  INSPECTION_FAILED = 'INSPECTION_FAILED',
  REFUND_ISSUED = 'REFUND_ISSUED',
  REJECTED = 'REJECTED',
  CANCELLED = 'CANCELLED'
}

const ALLOWED_RETURN_TRANSITIONS: Record<ReturnRequestStatus, ReturnRequestStatus[]> = {
  [ReturnRequestStatus.SUBMITTED]: [ReturnRequestStatus.APPROVED, ReturnRequestStatus.REJECTED, ReturnRequestStatus.CANCELLED],
  [ReturnRequestStatus.APPROVED]: [ReturnRequestStatus.RETURN_LABEL_SENT, ReturnRequestStatus.CANCELLED],
  [ReturnRequestStatus.RETURN_LABEL_SENT]: [ReturnRequestStatus.PACKAGE_RECEIVED, ReturnRequestStatus.CANCELLED],
  [ReturnRequestStatus.PACKAGE_RECEIVED]: [ReturnRequestStatus.INSPECTION_PASSED, ReturnRequestStatus.INSPECTION_FAILED],
  [ReturnRequestStatus.INSPECTION_PASSED]: [ReturnRequestStatus.REFUND_ISSUED],
  [ReturnRequestStatus.INSPECTION_FAILED]: [ReturnRequestStatus.REJECTED],
  [ReturnRequestStatus.REFUND_ISSUED]: [],
  [ReturnRequestStatus.REJECTED]: [],
  [ReturnRequestStatus.CANCELLED]: []
};

export class ReturnStateMachine {
  public static canTransition(current: ReturnRequestStatus, target: ReturnRequestStatus): boolean {
    const allowed = ALLOWED_RETURN_TRANSITIONS[current] || [];
    return allowed.includes(target);
  }

  public static transition(current: ReturnRequestStatus, target: ReturnRequestStatus): ReturnRequestStatus {
    if (!this.canTransition(current, target)) {
      throw new Error(`Invalid return transition from ${current} to ${target}`);
    }
    return target;
  }
}
