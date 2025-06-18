# app/controllers/documents_controller.rb
class DocumentsController < ApplicationController
  before_action :require_login

  def download
    @document = Document.find(params[:id])
    base_directory = Rails.root.join("public", "uploads")
    path_to_file = File.join(base_directory, @document.name)

    # Logging for troubleshooting
    Rails.logger.info "Attempting to download file..."
    Rails.logger.info "Base Directory: #{base_directory}"
    Rails.logger.info "Document Name: #{@document.name}"
    Rails.logger.info "Full Path to File: #{path_to_file}"

    if File.exist?(path_to_file)
        Rails.logger.info "File exists. Sending file: #{path_to_file}"
        send_file path_to_file,
                filename: @document.file_path.presence || "document",
                type: "application/octet-stream"
    else
        Rails.logger.error "File not found: #{path_to_file}"
        flash[:alert] = "File not found: #{path_to_file}"
        redirect_back(fallback_location: root_path)
    end
end


  private

  def require_login
    unless current_user
      redirect_to login_path, alert: "Please log in first."
    end
  end
end
