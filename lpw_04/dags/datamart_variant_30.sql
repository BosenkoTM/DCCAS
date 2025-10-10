-- Витрина данных для анализа президентов США
-- Вариант задания №30
-- Создает VIEW с полями: president, party, inauguration_age, years_in_office

CREATE OR REPLACE VIEW us_presidents_datamart AS
SELECT 
    president,
    party,
    inauguration_age,
    years_in_office
FROM (
    SELECT 
        president,
        party,
        -- Расчет возраста при инаугурации на основе дат начала и конца срока
        CASE 
            WHEN start_date ~ '^\d{4}' THEN 
                EXTRACT(YEAR FROM AGE(
                    CASE 
                        WHEN start_date ~ '^\d{4}-\d{2}-\d{2}' THEN start_date::DATE
                        WHEN start_date ~ '^\d{4}-\d{2}' THEN start_date || '-01'::DATE
                        WHEN start_date ~ '^\d{4}' THEN start_date || '-01-01'::DATE
                        ELSE NULL
                    END,
                    '1750-01-01'::DATE  -- Примерная дата рождения для расчета
                ))
            ELSE NULL
        END as inauguration_age,
        
        -- Расчет количества лет в офисе
        CASE 
            WHEN start_date ~ '^\d{4}' AND end_date ~ '^\d{4}' THEN 
                EXTRACT(YEAR FROM AGE(
                    CASE 
                        WHEN end_date ~ '^\d{4}-\d{2}-\d{2}' THEN end_date::DATE
                        WHEN end_date ~ '^\d{4}-\d{2}' THEN end_date || '-01'::DATE
                        WHEN end_date ~ '^\d{4}' THEN end_date || '-01-01'::DATE
                        ELSE NULL
                    END,
                    CASE 
                        WHEN start_date ~ '^\d{4}-\d{2}-\d{2}' THEN start_date::DATE
                        WHEN start_date ~ '^\d{4}-\d{2}' THEN start_date || '-01'::DATE
                        WHEN start_date ~ '^\d{4}' THEN start_date || '-01-01'::DATE
                        ELSE NULL
                    END
                ))
            ELSE NULL
        END as years_in_office
        
    FROM raw_us_presidents
    WHERE president IS NOT NULL 
      AND party IS NOT NULL
      AND president != ''
      AND party != ''
) subquery
WHERE inauguration_age IS NOT NULL 
  AND years_in_office IS NOT NULL
ORDER BY president;

-- Комментарий к витрине
COMMENT ON VIEW us_presidents_datamart IS 'Витрина данных для анализа президентов США. Содержит информацию о президентах, их партиях, возрасте при инаугурации и количестве лет в офисе.';
