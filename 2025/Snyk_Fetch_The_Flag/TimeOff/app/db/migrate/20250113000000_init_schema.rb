# db/migrate/20250113000000_init_schema.rb
class InitSchema < ActiveRecord::Migration[7.0]
  def change
    create_table :users do |t|
      t.string :email, null: false
      t.string :password_digest, null: false
      t.string :role, null: false, default: 'user'
      t.timestamps
    end

    create_table :employees do |t|
      t.string :first_name, null: false
      t.string :last_name, null: false
      t.string :title, null: false
      t.references :user, null: false, foreign_key: true
      t.timestamps
    end

    create_table :departments do |t|
      t.string :name, null: false
      t.references :manager, foreign_key: { to_table: :employees }, null: true
      t.timestamps
    end

    create_table :time_off_requests do |t|
      t.references :employee, null: false, foreign_key: true
      t.date :start_date, null: false
      t.date :end_date, null: false
      t.string :reason, null: false
      t.string :status, null: false, default: 'pending'
      t.timestamps
    end

    create_table :documents do |t|
      t.references :time_off_request, null: false, foreign_key: true
      t.string :name, null: false
      t.string :file_path, null: false
      t.timestamps
    end
  end
end
