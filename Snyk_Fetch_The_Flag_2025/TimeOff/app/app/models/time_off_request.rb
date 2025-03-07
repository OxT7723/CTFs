# app/models/time_off_request.rb
class TimeOffRequest < ApplicationRecord
  belongs_to :employee
  has_one :document, dependent: :destroy

  validates :start_date, :end_date, presence: true
  validates :status, inclusion: { in: %w[pending approved denied] }

  validate :end_date_after_start_date

  private

  def end_date_after_start_date
    return if start_date.blank? || end_date.blank?
    if end_date < start_date
      errors.add(:end_date, "must be after start date")
    end
  end
end
