"""
ひとり親の実装
"""

from openfisca_core.periods import MONTH, DAY
from openfisca_core.variables import Variable

from openfisca_japan.entities import 世帯


class 配偶者がいるがひとり親に該当(Variable):
    value_type = bool
    default_value = False
    entity = 世帯
    definition_period = DAY
    label = "配偶者がいるがひとり親に該当"


class ひとり親(Variable):
    value_type = bool
    entity = 世帯
    definition_period = DAY
    label = "ひとり親に該当するか否か"
    reference = "https://www.city.shibuya.tokyo.jp/kodomo/teate/hitorioya/hitorioya_teate.html"
    documentation = """
    渋谷区の児童扶養手当制度

    - 〒150-8010 東京都渋谷区宇田川町1-1
    - 渋谷区子ども青少年課子育て給付係
    - 03-3463-2558
    """

    def formula(対象世帯, 対象期間, parameters):
        配偶者なし = 対象世帯.nb_persons(世帯.配偶者) == 0

        return 配偶者なし + 対象世帯("配偶者がいるがひとり親に該当", 対象期間)


class 夫と離別死別(Variable):
    value_type = bool
    default_value = False
    entity = 世帯
    definition_period = DAY
    label = "夫と離別・死別しているか否か"
    reference = "https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1170.htm"


class 寡婦(Variable):
    value_type = bool
    entity = 世帯
    definition_period = DAY
    label = "寡婦に該当するか否か"
    reference = "https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1170.htm"

    def formula(対象世帯, 対象期間, parameters):
        子供がいない = 対象世帯.nb_persons(世帯.子) == 0
        return 子供がいない * 対象世帯("夫と離別死別", 対象期間)
