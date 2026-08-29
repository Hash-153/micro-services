import { ReturnStateMachine, ReturnRequestStatus } from '../src/domain/refund-state-machine.js';

describe('Order Return & RMA State Machine Suite', () => {
  it('should allow valid return progression', () => {
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.SUBMITTED, ReturnRequestStatus.APPROVED)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.APPROVED, ReturnRequestStatus.RETURN_LABEL_SENT)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.RETURN_LABEL_SENT, ReturnRequestStatus.PACKAGE_RECEIVED)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.PACKAGE_RECEIVED, ReturnRequestStatus.INSPECTION_PASSED)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.INSPECTION_PASSED, ReturnRequestStatus.REFUND_ISSUED)).toBe(true);
  });

  it('should reject illegal return state jump', () => {
    expect(() => {
      ReturnStateMachine.transition(ReturnRequestStatus.SUBMITTED, ReturnRequestStatus.REFUND_ISSUED);
    }).toThrow();
  });
});
