use anchor_lang::prelude::*;
use crate::errors::BidTraceError;
use crate::state::{AdminStatus, DualBidCommitment, Tender, TenderStatus};

#[derive(Accounts)]
pub struct ReviewAdministrativeCompliance<'info> {
    #[account(
        mut,
        has_one = authority,
        constraint = tender.status == TenderStatus::AdministrativeReview @ BidTraceError::TenderNotAdminReview,
    )]
    pub tender: Account<'info, Tender>,

    #[account(
        mut,
        seeds = [b"bid", tender.key().as_ref(), bid_commitment.bidder.as_ref()],
        bump = bid_commitment.bump,
    )]
    pub bid_commitment: Account<'info, DualBidCommitment>,

    pub authority: Signer<'info>,
}

pub fn handle_review_administrative_compliance(
    ctx: Context<ReviewAdministrativeCompliance>,
    passed: bool,
    rejection_code: u16,
) -> Result<()> {
    let clock = Clock::get()?;
    let tender = &mut ctx.accounts.tender;
    let bid = &mut ctx.accounts.bid_commitment;

    // Strict slot boundary: Administrative review must occur before or at deadline
    require!(
        clock.slot <= tender.admin_review_deadline_slot,
        BidTraceError::AdminReviewDeadlineExceeded
    );

    // Prevent duplicate review / score mutation
    require!(
        bid.admin_status == AdminStatus::Pending,
        BidTraceError::AdminAlreadyReviewed
    );

    if passed {
        bid.admin_status = AdminStatus::Passed;
        bid.admin_rejection_code = 0;
        tender.total_admin_passed = tender.total_admin_passed.checked_add(1).unwrap();
    } else {
        bid.admin_status = AdminStatus::Failed;
        bid.admin_rejection_code = rejection_code;
    }

    msg!(
        "Administrative compliance evaluated: bidder={}, status={:?}, rejection_code={}, total_admin_passed={}",
        bid.bidder,
        bid.admin_status,
        bid.admin_rejection_code,
        tender.total_admin_passed
    );

    Ok(())
}
