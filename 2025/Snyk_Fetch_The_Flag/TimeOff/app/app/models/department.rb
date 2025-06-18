# app/models/department.rb
class Department < ApplicationRecord
  belongs_to :manager, class_name: 'Employee', optional: true
  
  has_many :employees, dependent: :nullify
  
  validates :name, presence: true
end
