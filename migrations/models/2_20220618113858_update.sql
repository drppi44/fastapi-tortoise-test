-- upgrade --
ALTER TABLE "carmodel" RENAME TO "cars";
ALTER TABLE "event" RENAME TO "events";
-- downgrade --
ALTER TABLE "cars" RENAME TO "carmodel";
ALTER TABLE "events" RENAME TO "event";
