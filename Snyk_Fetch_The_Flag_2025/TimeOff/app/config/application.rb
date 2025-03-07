# app/config/application.rb
require_relative 'boot'

require 'rails/all'

Bundler.require(*Rails.groups)

module InternalApp
  class Application < Rails::Application
    config.load_defaults 7.0
    config.eager_load = false
    config.log_level = :info

  end
end


