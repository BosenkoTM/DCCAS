-- ЛР № 3: образец структуры витрины, НЕ готовый SQL для любого варианта.
-- Перед выполнением адаптируйте названия таблиц, полей и ключи к своей предметной области.
-- Нельзя соединять таблицы 1:N без контроля гранулярности и количества строк.

-- CREATE OR REPLACE VIEW public.business_datamart AS
-- SELECT
--     entity_id,
--     metric_date,
--     business_metric
-- FROM public.stg_business_source
-- WHERE business_metric IS NOT NULL;

-- Контроль после создания витрины:
-- SELECT COUNT(*) AS datamart_rows FROM public.business_datamart;
-- SELECT SUM(business_metric) AS total_metric FROM public.business_datamart;
