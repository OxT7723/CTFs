class FilesController < ApplicationController
  def show
    path = params[:path]

    begin
      content = File.read(path)
      render plain: content
    rescue => e
      render plain: "Error reading file: #{e}"
    end
  end
end
