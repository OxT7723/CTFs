Rails.application.configure do
  config.log_level = :info
  
  logger           = ActiveSupport::Logger.new(STDOUT)
  logger.formatter = config.log_formatter
  config.logger    = logger
end