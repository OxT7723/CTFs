# app/models/document.rb
class Document < ApplicationRecord
    belongs_to :time_off_request
end
