# lib/tasks/seed_and_consolidate.rake
namespace :db do
  desc "Consolidate migrations and seed the database"
  task consolidate_and_seed: :environment do
    Rake::Task['db:drop'].invoke
    Rake::Task['db:create'].invoke
    Rake::Task['db:migrate'].invoke
    Rake::Task['db:seed'].invoke

    puts "Database has been consolidated and seeded successfully."
  end
end
