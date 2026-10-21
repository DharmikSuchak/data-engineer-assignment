-- 1. Acacia taxonomy entries (one entry per distinct species name).
SELECT COUNT(DISTINCT species) AS acacia_types
FROM taxonomy
WHERE species LIKE 'Acacia %';

-- 2. The wheat species with the longest complete rfamseq entry.
SELECT t.species, r.rfamseq_acc, r.length AS sequence_length
FROM taxonomy AS t
JOIN rfamseq AS r ON r.ncbi_id = t.ncbi_id
WHERE t.species LIKE 'Triticum %'
ORDER BY r.length DESC
LIMIT 1;

-- 3 and 4. Ninth page of families, 15 per page: (9 - 1) * 15 = 120.
-- Check each linked sequence length once before joining back to its families.
SELECT f.rfam_acc, f.rfam_id, MAX(r.length) AS max_sequence_length
FROM (SELECT DISTINCT rfamseq_acc FROM full_region) AS ids
STRAIGHT_JOIN rfamseq AS r ON r.rfamseq_acc = ids.rfamseq_acc
STRAIGHT_JOIN full_region AS fr ON fr.rfamseq_acc = ids.rfamseq_acc
STRAIGHT_JOIN family AS f ON f.rfam_acc = fr.rfam_acc
WHERE r.length > 1000000
GROUP BY f.rfam_acc, f.rfam_id
ORDER BY max_sequence_length DESC, f.rfam_acc
LIMIT 15 OFFSET 120;
