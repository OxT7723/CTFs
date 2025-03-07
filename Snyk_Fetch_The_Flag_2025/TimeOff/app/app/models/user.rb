class User < ApplicationRecord
  has_secure_password
  has_one :employee

  validates :email, presence: true, uniqueness: true
end
