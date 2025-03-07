# app/models/employee.rb
class Employee < ApplicationRecord
  belongs_to :user
  has_many :time_off_requests, dependent: :destroy
  has_many :managed_departments, class_name: 'Department', foreign_key: 'manager_id'

  validates :first_name, :last_name, :title, presence: true
end
